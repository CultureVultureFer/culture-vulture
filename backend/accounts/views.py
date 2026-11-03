"""
HTTP API za F-001. Svi odgovori su JSON (osim Google redirecta).

Prijava i registracija su ISKLJUČIVO preko Googlea (OpenID Connect), za
korisnike i za organizatore. Nema registracije ni prijave lozinkom, pa
nemamo lozinke koje bi trebalo čuvati, resetirati ili potvrđivati email:
Google je već potvrdio da je email od te osobe.
(Iznimka: superuser napravljen naredbom `createsuperuser` ima lozinku, ali
samo za Django /admin, ne za aplikaciju.)

Kako React održava prijavu: nakon Google prijave Django postavi kolačić
`sessionid` (HttpOnly). Preglednik ga šalje uz svaki idući zahtjev, a Django
iz njega zna tko je `request.user`. React tokene nikad ne vidi i ne sprema.

Svi POST zahtjevi trebaju CSRF token (header X-CSRFToken). React ga dobije
pozivom GET /api/auth/csrf/ (vidi frontend/src/api/auth.js).

Format greške je uvijek:
    400  {"errors": {"name": ["..."]}}
    401  {"errors": {"__all__": ["Not logged in."]}}
pa ih frontend može prikazati uz odgovarajuće polje forme.
"""

import json
from urllib.parse import urlencode

from authlib.integrations.base_client import OAuthError
from django.conf import settings
from django.contrib.auth import login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .forms import OrganizerForm
from .oidc import google
from .services import GoogleLoginError, OrganizerError, become_organizer, login_with_google

MODEL_BACKEND = "django.contrib.auth.backends.ModelBackend"
SESSION_NEXT_KEY = "auth_next"


# ------------------------------------------------------------------------------
# Pomoćne funkcije
# ------------------------------------------------------------------------------

def user_payload(user) -> dict:
    """Što frontend dobiva o korisniku. Tokeni NIKAD ne idu van."""
    return {
        "id": user.pk,
        "username": user.username,
        "email": user.email,
        "role": user.role.name,
    }


def _errors(errors: dict, status: int = 400) -> JsonResponse:
    return JsonResponse({"errors": errors}, status=status)


def _form_errors(form) -> JsonResponse:
    data = form.errors.get_json_data()
    return _errors({field: [e["message"] for e in errs] for field, errs in data.items()})


def _not_logged_in() -> JsonResponse:
    return _errors({"__all__": ["Not logged in."]}, status=401)


def _json_body(request) -> dict | None:
    """
    Frontend šalje JSON. Prihvaćamo i obične forme (request.POST) da se API
    može isprobati iz Django test klijenta ili curl-a bez JSON-a.
    """
    if request.content_type == "application/json":
        try:
            data = json.loads(request.body or b"{}")
        except json.JSONDecodeError:
            return None
        return data if isinstance(data, dict) else None
    return request.POST.dict()


def _safe_next(value: str | None) -> str:
    """Samo relativne putanje; inače ?next=https://zlo.com = open redirect."""
    if value and value.startswith("/") and url_has_allowed_host_and_scheme(value, allowed_hosts=set()):
        return value
    return "/"


def _frontend_redirect(path: str = "/", **params) -> HttpResponseRedirect:
    url = settings.FRONTEND_URL.rstrip("/") + path
    if params:
        url += "?" + urlencode(params)
    return HttpResponseRedirect(url)


# ------------------------------------------------------------------------------
# Google (OpenID Connect, Authorization Code + PKCE): registracija i prijava
# ------------------------------------------------------------------------------

@require_GET
def google_login_view(request):
    """
    GET /api/auth/google/login/?next=/neka/stranica

    Frontend ovamo šalje PUNU NAVIGACIJU (window.location), ne fetch():
    korisnik mora vidjeti Googleovu stranicu za prijavu.
    Prva prijava automatski stvara račun (uloga USER).

    Organizator: frontend ga šalje ovamo s next=/register/organizer (ili
    kako se već zove stranica s Karlovim obrascem), a nakon prijave taj
    obrazac pošalje naziv organizacije na register/organizer/.
    """
    request.session[SESSION_NEXT_KEY] = _safe_next(request.GET.get("next"))
    return google.authorize_redirect(
        request,
        settings.OIDC_GOOGLE_REDIRECT_URI,
        # Uvijek ponudi odabir računa (dijeljena računala, više Google računa).
        prompt="select_account",
    )


@require_GET
def google_callback_view(request):
    """GET /api/auth/google/callback/?code=...&state=...  (zove ga Google)"""
    next_path = request.session.pop(SESSION_NEXT_KEY, "/")

    try:
        # Provjeri state, zamijeni code (+ PKCE verifier + client_secret) za
        # tokene, provjeri id_token (potpis, iss, aud, exp, nonce).
        token = google.authorize_access_token(request)
    except OAuthError as exc:
        code = "cancelled" if exc.error == "access_denied" else "oidc_error"
        return _frontend_redirect("/login", auth_error=code)
    except Exception:
        # Google nedostupan i slično. U produkciji ovdje dodati logging.
        return _frontend_redirect("/login", auth_error="oidc_error")

    claims = token.get("userinfo")
    if not claims:
        # Bez id_tokena to nije OIDC prijava nego samo OAuth pristup API-ju.
        return _frontend_redirect("/login", auth_error="oidc_error")

    try:
        user = login_with_google(dict(claims), token, current_user=request.user)
    except GoogleLoginError as exc:
        return _frontend_redirect("/login", auth_error=exc.code)

    # login() mijenja ključ sesije (zaštita od session fixation napada).
    login(request, user, backend=MODEL_BACKEND)
    return _frontend_redirect(next_path)


# ------------------------------------------------------------------------------
# Organizator
# ------------------------------------------------------------------------------

@require_POST
def register_organizer_view(request):
    """
    POST /api/auth/register/organizer/  {name}  -> 200 organizator

    Korisnik mora biti prijavljen Googleom. Upiše naziv organizacije i dobije
    ulogu ORGANIZER. Email i lozinka se NE šalju: email je onaj s Googlea,
    a lozinke nema.
    """
    if not request.user.is_authenticated:
        return _not_logged_in()

    data = _json_body(request)
    if data is None:
        return _errors({"__all__": ["Invalid JSON."]})

    form = OrganizerForm(data, user=request.user)
    if not form.is_valid():
        return _form_errors(form)

    try:
        user = become_organizer(request.user, form.cleaned_data["name"])
    except OrganizerError as exc:
        return _errors({"__all__": [str(exc)]})
    except IntegrityError:
        # Netko je isti naziv zauzeo u istom trenutku.
        return _errors({"name": ["An organization with this name already exists."]})

    return JsonResponse(user_payload(user))


# ------------------------------------------------------------------------------
# Sesija
# ------------------------------------------------------------------------------

@require_GET
def me_view(request):
    """GET /api/auth/me/  -> 200 korisnik | 401. React ovo zove pri pokretanju."""
    if not request.user.is_authenticated:
        return _not_logged_in()
    return JsonResponse(user_payload(request.user))


@require_POST
def logout_view(request):
    """
    POST /api/auth/logout/  -> 204

    POST + CSRF, a ne GET: inače bi svaka tuđa stranica mogla korisnika
    odjaviti s <img src="/api/auth/logout/">.
    Korisnik ostaje prijavljen kod Googlea, kao i kod svih "Prijava s
    Googleom" gumba; Google ni ne nudi OIDC odjavu (end_session_endpoint).
    """
    logout(request)
    return HttpResponse(status=204)


@require_GET
@ensure_csrf_cookie
def csrf_view(request):
    """GET /api/auth/csrf/  -> 204 i postavljen kolačić `csrftoken`."""
    return HttpResponse(status=204)

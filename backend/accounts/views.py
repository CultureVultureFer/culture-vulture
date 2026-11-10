import json
from urllib.parse import urlencode

from authlib.integrations.base_client import OAuthError
from django.conf import settings
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .forms import OrganizationRegisterForm
from .oidc import google
from .services import GoogleLoginError, login_with_google, register_organizer_with_google

MODEL_BACKEND = "django.contrib.auth.backends.ModelBackend"
# Will be changed later, when we decide where users should be rerouted after login
FRONTEND_REDIRECT_PATH = "/hello"
# Ključevi sesije koji se čuvaju između zahtjeva za registraciju organizatora i Google callbacka
AUTH_INTENT = "auth_intent"
PENDING_ORGANIZATION_NAME = "pending_organization_name"
ORGANIZATION_INTENT = "organization"

def user_payload(user):
    return {
        "id": user.pk,
        "username": user.username,
        "email": user.email,
        "role": user.role.name,
    }


def _errors(errors, status=400):
    return JsonResponse({"errors": errors}, status=status)


def _not_logged_in():
    return _errors({"__all__": ["Not logged in."]}, status=401)

def _frontend_redirect(path="/", **params):
    url = settings.FRONTEND_URL.rstrip("/") + path
    if params:
        url += "?" + urlencode(params)
    return HttpResponseRedirect(url)


def _google_authorize_redirect(request):
    return google.authorize_redirect(
        request,
        settings.OIDC_GOOGLE_REDIRECT_URI,
        prompt="select_account",
    )


def _pop_pending_organization(session):
    return session.pop(AUTH_INTENT, None), session.pop(PENDING_ORGANIZATION_NAME, None)


def _read_json_object(request):
    try:
        body = json.loads(request.body)
    except ValueError:
        return None
    return body if isinstance(body, dict) else None


@require_GET
def google_login_view(request):
    # Obična prijava uvijek ostaje obična prijava, čak i nakon odustale registracije organizatora.
    _pop_pending_organization(request.session)
    return _google_authorize_redirect(request)


@require_GET
def google_callback_view(request):
    next_path = FRONTEND_REDIRECT_PATH
    # Odmah pročitaj i obriši, tako da ove vrijednosti vrijede samo za jedan pokušaj.
    intent, organization_name = _pop_pending_organization(request.session)

    try:
        token = google.authorize_access_token(request)
    except OAuthError as exc:
        code = "cancelled" if exc.error == "access_denied" else "oidc_error"
        return _frontend_redirect("/login", auth_error=code)
    except Exception:
        return _frontend_redirect("/login", auth_error="oidc_error")

    claims = token.get("userinfo")
    if not claims:
        return _frontend_redirect("/login", auth_error="oidc_error")

    try:
        if intent == ORGANIZATION_INTENT:
            if not organization_name:
                raise GoogleLoginError("organization_not_registered")
            user = register_organizer_with_google(dict(claims), organization_name, current_user=request.user)
        else:
            user = login_with_google(dict(claims), current_user=request.user)
    except GoogleLoginError as exc:
        return _frontend_redirect("/login", auth_error=exc.code)

    login(request, user, backend=MODEL_BACKEND)
    return _frontend_redirect(next_path)


@require_http_methods(["GET", "POST"])
def organization_register_view(request):
    # Jednokratna registracija organizatora na jednoj adresi:
    #   POST {"name": ...} provjeri naziv (200 / 400) i zapamti ga u sesiji,
    #   GET zatim pošalje preglednik na Google. Kasnije prijave idu kroz običnu Google prijavu.
    if request.method == "GET":
        return _organization_register_google(request)
    return _organization_register_name(request)


def _organization_register_google(request):
    if request.session.get(AUTH_INTENT) != ORGANIZATION_INTENT or not request.session.get(PENDING_ORGANIZATION_NAME):
        return _frontend_redirect("/login", auth_error="organization_not_registered")
    return _google_authorize_redirect(request)


def _organization_register_name(request):
    body = _read_json_object(request)
    if body is None:
        return _errors({"__all__": ["Invalid JSON."]})

    if request.user.is_authenticated:
        return _errors({"__all__": ["You already have an account."]})

    form = OrganizationRegisterForm(data=body)
    if not form.is_valid():
        return _errors(form.errors)

    request.session[AUTH_INTENT] = ORGANIZATION_INTENT
    request.session[PENDING_ORGANIZATION_NAME] = form.cleaned_data["name"]
    return JsonResponse({"redirect": reverse("accounts:organization-register")})


@require_GET
def me_view(request):
    if not request.user.is_authenticated:
        return _not_logged_in()
    return JsonResponse(user_payload(request.user))


@require_POST
def logout_view(request):
    logout(request)
    return HttpResponse(status=204)


@require_GET
@ensure_csrf_cookie
def csrf_view(request):
    return HttpResponse(status=204)

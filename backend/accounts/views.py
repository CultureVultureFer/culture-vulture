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


def user_payload(user) -> dict:
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
    if request.content_type == "application/json":
        try:
            data = json.loads(request.body or b"{}")
        except json.JSONDecodeError:
            return None
        return data if isinstance(data, dict) else None
    return request.POST.dict()


def _safe_next(value: str | None) -> str:
    if value and value.startswith("/") and url_has_allowed_host_and_scheme(value, allowed_hosts=set()):
        return value
    return "/"


def _frontend_redirect(path: str = "/", **params) -> HttpResponseRedirect:
    url = settings.FRONTEND_URL.rstrip("/") + path
    if params:
        url += "?" + urlencode(params)
    return HttpResponseRedirect(url)


@require_GET
def google_login_view(request):
    request.session[SESSION_NEXT_KEY] = _safe_next(request.GET.get("next"))
    return google.authorize_redirect(
        request,
        settings.OIDC_GOOGLE_REDIRECT_URI,
        prompt="select_account",
    )


@require_GET
def google_callback_view(request):
    next_path = request.session.pop(SESSION_NEXT_KEY, "/")

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
        user = login_with_google(dict(claims), token, current_user=request.user)
    except GoogleLoginError as exc:
        return _frontend_redirect("/login", auth_error=exc.code)

    login(request, user, backend=MODEL_BACKEND)
    return _frontend_redirect(next_path)


@require_POST
def register_organizer_view(request):
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
        return _errors({"name": ["An organization with this name already exists."]})

    return JsonResponse(user_payload(user))


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

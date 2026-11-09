from urllib.parse import urlencode

from authlib.integrations.base_client import OAuthError
from django.conf import settings
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .oidc import google
from .services import GoogleLoginError, login_with_google

MODEL_BACKEND = "django.contrib.auth.backends.ModelBackend"
# Will be changed later, when we decide where users should be rerouted after login
FRONTEND_REDIRECT_PATH = "/hello"

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


@require_GET
def google_login_view(request):
    return google.authorize_redirect(
        request,
        settings.OIDC_GOOGLE_REDIRECT_URI,
        prompt="select_account",
    )


@require_GET
def google_callback_view(request):
    next_path = FRONTEND_REDIRECT_PATH

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

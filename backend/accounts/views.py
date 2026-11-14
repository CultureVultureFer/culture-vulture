from urllib.parse import urlencode

from authlib.integrations.base_client import OAuthError
from django.conf import settings
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .oidc import google
from .serializers import OrganizationRegisterSerializer, UserSerializer
from .services import GoogleLoginError, login_with_google, register_organizer_with_google

MODEL_BACKEND = "django.contrib.auth.backends.ModelBackend"
# Will be changed later, when we decide where users should be rerouted after login
FRONTEND_REDIRECT_PATH = "/hello"
# Session keys kept between the organizer registration request and the Google callback
AUTH_INTENT = "auth_intent"
PENDING_ORGANIZATION_NAME = "pending_organization_name"
ORGANIZATION_INTENT = "organization"


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


@api_view(["GET"])
def google_login_view(request):
    # A normal login always stays a normal login, even after an abandoned organizer registration.
    _pop_pending_organization(request.session)
    return _google_authorize_redirect(request)


@api_view(["GET"])
def google_callback_view(request):
    next_path = FRONTEND_REDIRECT_PATH
    # Read and clear right away so these values are valid for a single attempt only.
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


@api_view(["GET", "POST"])
def organization_register_view(request):
    # One-time organizer registration on a single URL:
    #   POST {"name": ...} validates the name (200 / 400) and remembers it in the session,
    #   GET then sends the browser to Google. Later logins use the normal Google login.
    if request.method == "GET":
        return _organization_register_google(request)
    return _organization_register_name(request)


def _organization_register_google(request):
    if request.session.get(AUTH_INTENT) != ORGANIZATION_INTENT or not request.session.get(PENDING_ORGANIZATION_NAME):
        return _frontend_redirect("/login", auth_error="organization_not_registered")
    return _google_authorize_redirect(request)


def _organization_register_name(request):
    if request.user.is_authenticated:
        return Response({"detail": "You already have an account."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = OrganizationRegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    request.session[AUTH_INTENT] = ORGANIZATION_INTENT
    request.session[PENDING_ORGANIZATION_NAME] = serializer.validated_data["name"]
    return Response({"redirect": reverse("accounts:organization-register")})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    return Response(UserSerializer(request.user).data)


@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT)


@ensure_csrf_cookie
@api_view(["GET"])
def csrf_view(request):
    return Response(status=status.HTTP_204_NO_CONTENT)

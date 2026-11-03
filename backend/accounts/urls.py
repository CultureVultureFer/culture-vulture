from django.urls import path

from . import views

app_name = "accounts"

# Nema register/ ni login/ s lozinkom: registracija i prijava su samo preko
# Googlea (google/login/). Organizator se nakon Google prijave registrira
# na register/organizer/ (samo naziv organizacije).
urlpatterns = [
    path("csrf/", views.csrf_view, name="csrf"),
    path("me/", views.me_view, name="me"),
    path("logout/", views.logout_view, name="logout"),
    path("google/login/", views.google_login_view, name="google-login"),
    # Puni URL ove rute mora biti upisan u Google Cloud Consoleu kao
    # "Authorized redirect URI" i u .env kao OIDC_GOOGLE_REDIRECT_URI.
    path("google/callback/", views.google_callback_view, name="google-callback"),
    path("register/organizer/", views.register_organizer_view, name="register-organizer"),
]

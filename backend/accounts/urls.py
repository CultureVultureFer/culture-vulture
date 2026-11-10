from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("csrf/", views.csrf_view, name="csrf"),
    path("me/", views.me_view, name="me"),
    path("logout/", views.logout_view, name="logout"),
    path("organization/register/", views.organization_register_view, name="organization-register"),
    path("google/login/", views.google_login_view, name="google-login"),    path("google/callback/", views.google_callback_view, name="google-callback"),
]

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # F-001: Google OIDC login/logout
    path('api/auth/', include('accounts.urls')),
    path("api/", include("events.urls")),
]

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Role, User


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(User)
class CultureVultureUserAdmin(UserAdmin):
    list_display = ("email", "username", "role", "is_active", "date_joined")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("email", "username")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("CultureVulture", {"fields": ("role",)}),
        ("Django permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "username", "role", "password1", "password2")}),
    )

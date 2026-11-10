from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count

from .models import Organization, Role, User


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "organizer_count", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(organizer_count=Count("organizers"))

    @admin.display(description="Organizers", ordering="organizer_count")
    def organizer_count(self, obj):
        return obj.organizer_count


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(User)
class CultureVultureUserAdmin(UserAdmin):
    list_display = ("email", "username", "role", "organization", "is_active", "date_joined")
    list_filter = ("role", "is_active", "is_staff")
    list_select_related = ("role", "organization")
    search_fields = ("email", "username", "organization__name")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("CultureVulture", {"fields": ("role", "organization")}),
        ("Django permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "username", "role", "password1", "password2")}),
    )

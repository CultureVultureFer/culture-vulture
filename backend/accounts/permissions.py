from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOrganizer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_organizer)


class IsAppAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_app_admin)


class IsOrganizerOrReadOnly(BasePermission):
    # Use on a view that serves both reading and writing on one URL:
    # GET is open to everyone, every other method needs the ORGANIZER role.
    # For a write-only view use IsOrganizer directly.
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or IsOrganizer().has_permission(request, view)

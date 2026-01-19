from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission:
    - Read permissions (GET, HEAD, OPTIONS) allowed to any user (even anonymous)
    - Write permissions (POST, PUT, PATCH, DELETE) allowed only to admin users
    """

    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in SAFE_METHODS:
            return True

        # Write permissions only for admin users
        return request.user and request.user.is_staff

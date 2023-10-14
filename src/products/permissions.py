from rest_framework.permissions import BasePermission

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsAdminOrSafeMethods(BasePermission):
    """
    The request is authenticated as an admin, or method is safe.
    """

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or
                request.user and
                request.user.is_staff):
            return True
        return False

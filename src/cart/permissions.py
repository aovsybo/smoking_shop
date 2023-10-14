from rest_framework.permissions import BasePermission

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsVerified(BasePermission):
    """
    The user is verified
    """
    message = 'Your account must be verified'

    def has_permission(self, request, view):
        if request.user and request.user.is_verified:
            return True
        return False

from rest_framework import permissions
from users.models import ROLE_ADMIN


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == ROLE_ADMIN))


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            (request.method in permissions.SAFE_METHODS)
            or (request.user.is_authenticated
                and (request.user.role == ROLE_ADMIN)
                )
        )

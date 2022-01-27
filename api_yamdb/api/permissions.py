from rest_framework import permissions

from users.models import ROLE_ADMIN

MODERATOR_METHODS = ('PATCH', 'DELETE')


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == 'admin'))


class IsAdminPe(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.role == 'admin'))


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return ((request.method in permissions.SAFE_METHODS)
                or (request.user.is_authenticated
                and request.user.role == 'admin')
                or (request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return ((request.method in permissions.SAFE_METHODS)
                or ((request.user.is_authenticated)
                and (request.user.role == 'admin'))
                or (request.user.is_superuser))


class IsAuthorOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return ((request.method in permissions.SAFE_METHODS)
                or (request.user.is_authenticated))

    def has_object_permission(self, request, view, obj):
        return (((request.method in MODERATOR_METHODS)
                and (request.user.role == 'moderator'))
                or (obj.author == request.user))


class OwnResourcePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                and request.user.is_anonymous
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'DELETE']:
            return (obj.author == request.user
                    or request.user.role in [request.user.ADMIN,
                                             request.user.role == 'moderator'])
        return True


class IsAuthorOrAdminOrModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if (request.user.is_staff
                    or request.user.role == 'admin'
                    or request.user.role == 'moderator'
                    or obj.author == request.user
                    or request.method == 'POST'):
                return True
        if request.method in permissions.SAFE_METHODS:
            return True


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            (request.method in permissions.SAFE_METHODS)
            or (request.user.is_authenticated
                and (request.user.role == ROLE_ADMIN)
                )
        )

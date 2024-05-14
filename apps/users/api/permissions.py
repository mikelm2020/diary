from rest_framework import permissions


class CreateUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Permitir a cualquier usuario realizar una solicitud POST (create)
        if view.action == "create":
            return True
        # Requiere autenticación para otros métodos
        return request.user and request.user.is_authenticated


class IsTenant(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and not request.user.is_owner
            and request.method in permissions.SAFE_METHODS
        )


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_owner


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

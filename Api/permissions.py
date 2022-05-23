from rest_framework import permissions


class IsSuperuserPermission(permissions.BasePermission):
    message = 'Page available only for superusers'

    def has_permission(self, request, view):
        user = request.user
        return user.is_active and user.is_superuser


class IsStaffPermission(permissions.BasePermission):
    message = 'Page available only for staffs'

    def has_permission(self, request, view):
        user = request.user
        return user.is_active and (user.staff or user.is_superuser)

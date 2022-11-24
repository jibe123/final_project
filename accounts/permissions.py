from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    message = "У вас недостаточно прав для этого действия!"

    def has_permission(self, request, view):
        return True if request.user.is_superuser else False

    def has_object_permission(self, request, view, obj):
        return True if request.user.is_superuser else False


class IsOfficer(BasePermission):
    message = "У вас недостаточно прав для этого действия!"

    def has_permission(self, request, view):
        return True if request.user.is_officer else False

    def has_object_permission(self, request, view, obj):
        return True if request.user.is_officer else False


class IsManagement(BasePermission):
    message = "У вас недостаточно прав для этого действия!"

    def has_permission(self, request, view):
        return True if request.user.is_management else False

    def has_object_permission(self, request, view, obj):
        return True if request.user.is_management else False
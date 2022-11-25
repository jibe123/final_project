from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    message = "Вы должны быть администратором для выполнения этого действия!"

    def has_permission(self, request, view):
        return True if request.user.is_superuser else False

    def has_object_permission(self, request, view, obj):
        return True if request.user.is_superuser else False


class IsManager(BasePermission):
    message = "Вы должны быть сотрудником для выполнения этого действия!"

    def has_permission(self, request, view):
        return True if request.user.is_manager else False

    def has_object_permission(self, request, view, obj):
        return True if request.user.is_manager else False
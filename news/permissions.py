from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    message = "У вас недостаточно прав для этого действия!"

    def has_permission(self, request, view):
        return True if request.user.is_superuser else False


class IsOfficer(BasePermission):
    message = "У вас недостаточно прав для этого действия!"

    def has_permission(self, request, view):
        return True if request.user.is_officer else False


class IsOwner(BasePermission):
    message = "У вас недостаточно прав для этого действия!"

    def has_object_permission(self, request, view, news_obj):
        return news_obj.owner.id == request.user.id


from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):

    def has_permission(self, request, view):
        return True if request.user.is_superuser else False

    def has_object_permission(self, request, view, news_obj):
        return True if request.user.is_superuser else False


class IsManager(BasePermission):

    def has_permission(self, request, view):
        return True if request.user.is_manager else False


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, news_obj):
        return news_obj.owner.id == request.user.id


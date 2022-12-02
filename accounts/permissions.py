from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        else:
            return True if request.user.is_superuser else False

    def has_object_permission(self, request, view, news_obj):
        if request.user.is_anonymous:
            return False
        else:
            return True if request.user.is_superuser else False


class IsManager(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        else:
            return True if request.user.is_manager else False

    def has_object_permission(self, request, view, obj):
        if request.user is AnonymousUser:
            return False
        else:
            return True if request.user.is_manager else False

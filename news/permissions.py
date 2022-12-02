from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        else:
            return True if request.user.is_manager else False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        else:
            return obj.owner.id == request.user.id

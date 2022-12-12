from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        else:
            return True if request.user.is_student else False

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        else:
            return True if request.user.is_student else False

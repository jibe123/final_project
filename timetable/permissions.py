from rest_framework.permissions import BasePermission

from accounts.models import Student


class IsCourseTeacher(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return True if request.user.is_teacher else False

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        return True if request.user == \
                       obj.course.teacher else False


class IsCourseStudent(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return True if request.user.is_student else False

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        student = Student.objects.get(pk=request.user)
        return True if student.group in obj.course.groups.all() else False


class IsMaterialsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        return request.user == obj.owner

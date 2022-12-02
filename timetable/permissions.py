from rest_framework.permissions import BasePermission

from accounts.models import Student
from .models import Course


class IsCourseTeacher(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return True if request.user == \
                       request.data.get["course"].teacher else False

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        return True if request.user == \
                       request.data.get["course"].teacher else False


class IsCourseStudent(BasePermission):
    def has_permission(self, request, view, **kwargs):
        if request.user.is_anonymous:
            return False
        student = Student.objects.get(pk=request.user.id)
        course = Course.objects.get(pk=kwargs["pk"])
        return True if student.group in course.groups else False

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        student = Student.objects.get(pk=request.user.id)
        return True if student.group in obj.groups else False

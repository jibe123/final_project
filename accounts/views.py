from django.contrib.auth.models import Permission
from rest_framework import generics, viewsets

from .models import User, Student
from .permissions import IsSuperuser, IsManager
from .serializers import (
    CreateStudentSerializer,
    UserSerializer,
    PermissionSerializer,
    StudentSerializer)


class StudentCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CreateStudentSerializer
    queryset = User.objects.all()
    permission_classes = [IsSuperuser | IsManager]

    def get_serializer(self, instance=None, data=None, many=False, partial=False):
        if data is not None:
            if type(data) == list:
                return super(StudentCreateAPIView, self).get_serializer(
                    instance=instance, data=data, many=True, partial=partial)
            if type(data) == dict:
                return super(StudentCreateAPIView, self).get_serializer(
                    instance=instance, data=data, many=False, partial=partial)
        else:
            return super(StudentCreateAPIView, self).get_serializer(
                instance=instance, many=True, partial=partial)


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsSuperuser,)


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = (IsSuperuser,)

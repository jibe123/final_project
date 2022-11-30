from django.contrib.auth.models import Permission
from rest_framework import generics, viewsets

from .models import User, Student, Group
from .permissions import IsSuperuser, IsManager
from .serializers import (
    NewStudentUserSerializer,
    UserSerializer,
    PermissionSerializer,
    StudentSerializer,
    GroupSerializer)


class StudentCreateAPIView(generics.ListCreateAPIView):
    serializer_class = NewStudentUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsSuperuser | IsManager]


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


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = (IsSuperuser,)

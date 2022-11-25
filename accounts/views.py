from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import (
    MyTokenObtainPairSerializer,
    CreateStudentSerializer,
    UserSerializer)
from .permissions import IsSuperuser, IsManager


class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


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


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import MyTokenObtainPairSerializer, NewUserSerializer, UserSerializer
from .permissions import IsOfficer, IsSuperuser


class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = NewUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsSuperuser | IsOfficer]


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, Student, Group, Officer
from .serializers import (
    MyTokenObtainPairSerializer,
    NewUserSerializer,
    UserSerializer,
    StudentSerializer,
    OfficerSerializer)
from .permissions import IsOfficer, IsSuperuser, IsManagement


class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserCreateAPIView(generics.ListCreateAPIView):
    serializer_class = NewUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsSuperuser]

    def get_serializer(self, instance=None, data=None, many=False, partial=False):
        if data is not None:
            if type(data) == list:
                return super(UserCreateAPIView, self).get_serializer(
                    instance=instance, data=data, many=True, partial=partial)
            if type(data) == dict:
                return super(UserCreateAPIView, self).get_serializer(
                    instance=instance, data=data, many=False, partial=partial)
        else:
            return super(UserCreateAPIView, self).get_serializer(
                instance=instance, many=True, partial=partial)


@api_view(['POST'])
@permission_classes([IsOfficer | IsSuperuser])
def set_student_groups(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        user_ids = serializer.validated_data.get('user_ids')
        group = serializer.validated_data.get('group')

        for user_id in user_ids:
            student = Student.objects.get(pk=user_id.pk)
            student.group_id = group
            student.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsManagement | IsSuperuser])
def set_officer_department(request):
    serializer = OfficerSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data.get('user')
        department = serializer.validated_data.get('department')
        officer = Officer.objects.get(pk=user.pk)
        officer.department_id = department
        officer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

from rest_framework import generics, viewsets, mixins

from .models import User, Student, Group
from .permissions import IsSuperuser, IsManager
import accounts.serializers as msz


class StudentCreateAPIView(generics.ListCreateAPIView):
    serializer_class = msz.NewStudentUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsSuperuser | IsManager]


class StudentViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = msz.StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsSuperuser | IsManager]


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = msz.GroupSerializer
    queryset = Group.objects.all()
    permission_classes = [IsSuperuser | IsManager]

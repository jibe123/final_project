from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from accounts.permissions import IsSuperuser, IsManager
from timetable.permissions import (
    IsCourseTeacher, IsCourseStudent, IsMaterialsOwner)
from accounts.models import Student
from .models import Course, CourseMaterials, Timetable
import timetable.serializers as msz


class TimetableViewSet(viewsets.ModelViewSet):
    serializer_class = msz.TimetableSerializer
    queryset = Timetable.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsSuperuser | IsManager]

        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsSuperuser | IsManager]

        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]


class CourseViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = msz.CourseSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            queryset = None
        elif self.request.user.is_superuser or self.request.user.is_manager:
            queryset = Course.objects.all()
        elif self.request.user.is_teacher:
            queryset = Course.objects.filter(teacher=self.request.user)
        elif self.request.user.is_student:
            queryset = Course.objects.filter(
                groups__id__exact=Student.objects.get(
                    pk=self.request.user).group_id)
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsSuperuser | IsManager]

        elif self.action == 'materials':
            permission_classes = [
                IsSuperuser | IsCourseTeacher | IsCourseStudent]

        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsSuperuser | IsManager]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    @csrf_exempt
    @action(detail=True, methods=['GET', 'POST'],
            serializer_class=msz.CourseMaterialsSerializer,
            parser_classes=(MultiPartParser, FormParser,),
            permission_classes=(
                IsSuperuser, IsCourseTeacher, IsCourseStudent,),
            url_path='materials', url_name='materials')
    def get_materials(self, request, *args, **kwargs):
        if request.method == 'GET':
            queryset = CourseMaterials.objects.filter(course=kwargs["pk"])
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            return Response(data)

        else:
            request.data["course"] = kwargs["pk"]
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CourseMaterialsViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = msz.CourseMaterialsSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            queryset = None
        elif self.request.user.is_superuser or self.request.user.is_manager:
            queryset = CourseMaterials.objects.all()
        elif self.request.user.is_teacher:
            queryset = CourseMaterials.objects.filter(
                course__in=Course.objects.filter(teacher=self.request.user))
        elif self.request.user.is_student:
            queryset = CourseMaterials.objects.filter(
                course__in=Student.objects.get(
                    pk=self.request.user).group.courses.all())
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsSuperuser | IsCourseTeacher]

        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsSuperuser | IsMaterialsOwner]

        elif self.action == 'retrieve':
            permission_classes = [
                IsSuperuser | IsCourseTeacher | IsCourseStudent]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsSuperuser, IsManager
from accounts.models import Group
from .models import Course, CourseMaterials, Timetable
import timetable.serializers as msz


class TimetableViewSet(viewsets.ModelViewSet):
    serializer_class = msz.CourseDaySerializer
    queryset = Timetable.objects.all()


class CourseViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser]
    serializer_class = msz.CourseSerializer
    queryset = Course.objects.all()


class CourseMaterialsViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = msz.CourseMaterialsSerializer
    queryset = CourseMaterials.objects.all()

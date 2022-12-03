from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
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
    serializer_class = msz.TimetableSerializer
    queryset = Timetable.objects.all()
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer,)
    template_name = 'base.html'

    def list(self, request, *args, **kwargs):
        data = self.get_serializer(self.get_queryset(), many=True).data
        return render(
            request,
            'timetable/timetable.html',
            {
                'data': data,
            }
        )


class CourseViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser]
    serializer_class = msz.CourseSerializer
    queryset = Course.objects.all()


class CourseMaterialsViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = msz.CourseMaterialsSerializer
    queryset = CourseMaterials.objects.all()

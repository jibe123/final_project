from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser

from accounts.permissions import IsSuperuser, IsManager
from accounts.models import Group
from .models import Course, CourseDay, CourseMaterials
import timetable.serializers as msz


@api_view(['POST'])
@permission_classes([IsSuperuser | IsManager])
def update_groups_data(request):
    serializer = msz.GroupsUpdateSerializer(data=request.data)
    if serializer.is_valid():
        input_data = serializer.validated_data
        course_id = input_data.get('course_id')
        mode = input_data.get('mode')
        group_id = input_data.get('group_id')
        try:
            course = Course.objects.get(pk=course_id)
            group = Group.objects.get(pk=group_id)
            if mode == "add":
                course.groups.add(group)
            else:
                course.groups.remove(group)
            return Response(status=status.HTTP_200_OK)
        except (Course.DoesNotExist, Group.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TimetableViewSet(viewsets.ModelViewSet):
    serializer_class = msz.CourseDaySerializer
    queryset = CourseDay.objects.all()


class CourseViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser]
    serializer_class = msz.CourseSerializer
    queryset = Course.objects.all()


class CourseMaterialsViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = msz.CourseMaterialsSerializer
    queryset = CourseMaterials.objects.all()

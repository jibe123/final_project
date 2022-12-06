from rest_framework import viewsets
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)

import assignments.models as md
import assignments.serializers as msz
from accounts.models import Student


class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = msz.AssignmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            assignment = serializer.create(data=request.data)
            if assignment:
                return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_manager:
            queryset = md.Assignment.objects.all()
        elif self.request.user.is_teacher:
            queryset = md.Assignment.objects.filter(teacher=self.request.user)
        else:
            queryset = md.Assignment.objects.filter(
                course__in=Student.objects.get(
                    pk=self.request.user).group.courses.all())
        return queryset

class AnswersViewSet(viewsets.ModelViewSet):
    serializer_class = msz.QuestionAnswersSerializer
    queryset = md.Question.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            question = serializer.create(
                ''
            )
            if question:
                return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST)


class GradedAssignmentListView(ListAPIView):
    serializer_class = msz.GradedAssignmentSerializer

    def get_queryset(self):
        queryset = md.GradedAssignment.objects.all()
        student = self.request.query_params.get('id', None)
        queryset = queryset.filter(student__id=student)
        return queryset


class GradedAssignmentCreateView(CreateAPIView):
    serializer_class = msz.GradedAssignmentSerializer
    queryset = md.GradedAssignment.objects.all()

    def post(self, request):
        serializer = msz.GradedAssignmentSerializer(data=request.data)
        serializer.is_valid()
        graded_assignment = serializer.create(request)
        if graded_assignment:
            return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST)

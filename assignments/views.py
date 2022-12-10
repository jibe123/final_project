from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

import assignments.models as md
import assignments.serializers as msz
from accounts.models import Student


class MyAssignmentListAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = msz.AssignmentsSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = md.Assignment.objects.filter(
            st_assignments__student=md.Student.objects.get(
                user=self.request.user))
        query = self.request.GET.get("q")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
            ).distinct()

        return queryset


class AssignmentListAPI(generics.ListAPIView):
    serializer_class = msz.AssignmentsListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = md.Assignment.objects.filter(
            course__in=Student.objects.get(
                pk=self.request.user).group.courses.all()).exclude(
            st_assignments__student=md.Student.objects.get(
                user=self.request.user))
        query = self.request.GET.get("q")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
            ).distinct()

        return queryset


class AssignmentDetailAPI(generics.RetrieveAPIView):
    serializer_class = msz.AssignmentDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        slug = self.kwargs["slug"]
        assignment = get_object_or_404(md.Assignment, slug=slug)
        last_question = None
        obj, created = md.StudentAssignment.objects.get_or_create(
            student=Student.objects.get(pk=self.request.user.pk), assignment=assignment)
        if created:
            for question in md.Question.objects.filter(
                    assignment=assignment):
                md.Answer.objects.create(
                    student=obj, question=question)
        else:
            last_question = md.Answer.objects.filter(
                student=obj, choice__isnull=False)
            if last_question.count() > 0:
                last_question = last_question.last().question.id
            else:
                last_question = None

        return Response({'assignment': self.get_serializer(
            assignment, context={'request': self.request}).data, 
                         'last_question_id': last_question})


class SaveAnswer(generics.RetrieveUpdateAPIView):
    queryset = md.Answer.objects.all()
    serializer_class = msz.TestAnswersSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(pk=self.kwargs.get("pk"))

    def patch(self, request, *args, **kwargs):
        student_id = request.data['student']
        question_id = request.data['question']
        choice_id = request.data['choice']

        student = get_object_or_404(md.StudentAssignment, id=student_id)
        question = get_object_or_404(md.Question, id=question_id)
        choice = get_object_or_404(md.Choice, id=choice_id)

        if student.completed:
            return Response({
                "message": "Это задание выполнено. "
                           "Вы не можете его выполнить повторно!"},
                status=status.HTTP_412_PRECONDITION_FAILED
            )

        obj = get_object_or_404(md.Answer, student=student, question=question)
        obj.choice = choice
        obj.save()

        return Response(self.get_serializer(obj).data)


class SubmitAssignmentAPI(generics.GenericAPIView):
    serializer_class = msz.AssignmentResultSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        student = request.data['student']
        student = get_object_or_404(md.StudentAssignment, student=student)

        if student.completed:
            return Response({
                "message": "Это задание выполнено. "
                           "Вы не можете его выполнить повторно!"
            },
                status=status.HTTP_412_PRECONDITION_FAILED
            )
        else:
            student.completed = True
            correct_answers = 0

            for answer in md.Answer.objects.filter(student=student):
                try:
                    choice = md.Choice.objects.get(question=answer.question,
                                                   is_correct=True)
                    if answer.choice == choice:
                        correct_answers += 1
                except md.Choice.DoesNotExist:
                    pass

            student.grade = int(correct_answers /
                                student.assignment.questions.count() * 100)
            student.save()

            return Response({
                "message": "Спасибо, ваши ответы приняты. "
            },
                status=status.HTTP_202_ACCEPTED
            )

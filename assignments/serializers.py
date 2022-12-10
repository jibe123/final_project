from rest_framework import serializers as sz
from accounts.models import Student
import assignments.models as md


class AssignmentsListSerializer(sz.ModelSerializer):
    class Meta:
        model = md.Assignment
        fields = ('id', 'title', 'teacher', 'course', 'questions_count',)
        read_only_fields = ('questions_count',)
    questions_count = sz.SerializerMethodField()

    def get_questions_count(self, obj):
        return obj.questions.count()


class ChoiceSerializer(sz.ModelSerializer):
    class Meta:
        model = md.Choice
        fields = ('id', 'question', 'text',)


class QuestionSerializer(sz.ModelSerializer):
    class Meta:
        model = md.Question
        fields = '__all__'
    choices = ChoiceSerializer(many=True)


class AnswersSerializer(sz.ModelSerializer):
    class Meta:
        model = md.Answer
        fields = '__all__'


class TestAnswersSerializer(sz.ModelSerializer):
    class Meta:
        model = md.Answer
        fields = ('id', 'student', 'answer_text', 'question', 'choice',)

    # def get_fields(self, *args, **kwargs):
    #     fields = super(TestAnswersSerializer, self).get_fields(*args, **kwargs)
    #     view = self.context['view']
    #     # question_id = md.Answer.objects.get(pk=view.kwargs.get('pk')).question.pk
    #     # student_asnmt_id = md.Answer.objects.get(pk=view.kwargs.get('pk')).student.pk
    #     # student_id = md.StudentAssignment.objects.get(pk=student_asnmt_id).student.pk
    #     fields['choice'].queryset = fields['choice'].queryset.filter(question=md.Answer.objects.get(pk=view.kwargs.get('pk')).question.pk)
    #     fields['student'].queryset = fields['student'].queryset.filter(student=md.StudentAssignment.objects.get(pk=md.Answer.objects.get(pk=view.kwargs.get('pk')).student.pk).student.pk)
    #     fields['question'].queryset = fields['question'].queryset.filter(pk=md.Answer.objects.get(pk=view.kwargs.get('pk')).question.pk)
    #     return fields


class AssignmentsSerializer(sz.ModelSerializer):
    completed = sz.SerializerMethodField()
    progress = sz.SerializerMethodField()
    questions_count = sz.SerializerMethodField()
    grade = sz.SerializerMethodField()
    graded = sz.SerializerMethodField()

    class Meta:
        model = md.Assignment
        fields = ('id', 'title', 'questions_count',
                  'completed', 'grade', 'progress', 'graded')
        read_only_fields = ('questions_count', 'completed', 'progress', 'graded')

    def get_completed(self, obj):
        try:
            student = md.StudentAssignment.objects.get(
                student=Student.objects.get(
                    pk=self.context['request'].user.pk), assignment=obj)
            return student.completed
        except md.StudentAssignment.DoesNotExist:
            return None

    def get_progress(self, obj):
        try:
            student = md.StudentAssignment.objects.get(
                student=Student.objects.get(
                    pk=self.context['request'].user.pk), assignment=obj)
            if student.completed is False:
                questions_answered = md.Answer.objects.filter(
                    student=student, choice__isnull=False).count()
                total_questions = obj.questions.all().count()
                return str(questions_answered / total_questions * 100)+'%'
            return None
        except md.StudentAssignment.DoesNotExist:
            return None

    def get_questions_count(self, obj):
        return obj.questions.all().count()

    def get_grade(self, obj):
        try:
            student = md.StudentAssignment.objects.get(
                student=Student.objects.get(
                    pk=self.context['request'].user.pk), assignment=obj)
            if student.completed is True:
                return student.grade
            return None
        except md.StudentAssignment.DoesNotExist:
            return None

    def get_graded(self, obj):
        try:
            student = md.StudentAssignment.objects.get(
                student=Student.objects.get(
                    pk=self.context['request'].user.pk), assignment=obj)
            return student.graded
        except md.StudentAssignment.DoesNotExist:
            return None


class StudentAssignmentSerializer(sz.ModelSerializer):
    answers = AnswersSerializer(many=True)

    class Meta:
        model = md.StudentAssignment
        fields = '__all__'


class AssignmentDetailSerializer(sz.ModelSerializer):
    student_set = sz.SerializerMethodField()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = md.Assignment
        fields = '__all__'

    def get_student_set(self, obj):
        try:
            student = md.StudentAssignment.objects.get(
                student=Student.objects.get(
                    pk=self.context['request'].user.pk), assignment=obj)
            serializer = StudentAssignmentSerializer(student)
            return serializer.data
        except md.StudentAssignment.DoesNotExist:
            return None


class AssignmentResultSerializer(sz.ModelSerializer):
    grade = sz.HiddenField(default=0)

    class Meta:
        model = md.StudentAssignment
        fields = '__all__'

    # def get_fields(self, *args, **kwargs):
    #     fields = super(
    #         AssignmentResultSerializer, self).get_fields(*args, **kwargs)
    #     view = self.context['view']
    #     assignment_id = md.Assignment.objects.get(
    #         slug=view.kwargs.get('slug'))
    #     student_asnmt_id = md.StudentAssignment.objects.get(
    #         student=self.context['request'].user.pk)
    #     fields['assignment'].queryset = \
    #         fields['assignment'].queryset.filter(pk=view.kwargs.get('slug'))
    #     fields['student'].queryset = \
    #         fields['student'].queryset.filter(
    #             st_assignments=self.context['request'].user.pk)
    #     return fields

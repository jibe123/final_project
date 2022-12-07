from rest_framework import serializers as sz
from accounts.models import User, Student
import assignments.models as md


class AssignmentsListSerializer(sz.ModelSerializer):
    class Meta:
        model = md.Assignment
        fields = ('id', 'title', 'teacher', 'course', 'questions_count',)
        read_only_fields = ('questions_count',)
    questions_count = sz.SerializerMethodField()

    def get_questions_count(self, obj):
        return obj.question_set.all().count()


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


class AssignmentsSerializer(sz.ModelSerializer):
    completed = sz.SerializerMethodField()
    progress = sz.SerializerMethodField()
    questions_count = sz.SerializerMethodField()
    score = sz.SerializerMethodField()

    class Meta:
        model = md.Assignment
        fields = ('id', 'title', 'questions_count',
                  'completed', 'grade', 'progress')
        read_only_fields = ('questions_count', 'completed', 'progress',)

    def get_completed(self, obj):
        try:
            student = md.StudentAssignment.objects.get(
                student=self.context['request'].user, assignment=obj)
            return student.completed
        except md.StudentAssignment.DoesNotExist:
            return None

    def get_progress(self, obj):
        try:
            student = md.StudentAssignment.objects.get(
                student=self.context['request'].user, assignment=obj)
            if student.completed is False:
                questions_answered = md.Answer.objects.filter(
                    student=student, answer__isnull=False).count()
                total_questions = obj.question_set.all().count()
                return int(questions_answered / total_questions)
            return None
        except md.StudentAssignment.DoesNotExist:
            return None

    def get_questions_count(self, obj):
        return obj.question_set.all().count()

    def get_grade(self, obj):
        try:
            student = md.StudentAssignment.objects.get(
                student=self.context['request'].user, assignment=obj)
            if student.completed is True:
                return student.grade
            return None
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
    student_set = sz.SerializerMethodField()
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = md.Assignment
        fields = '__all__'

    def get_student_set(self, obj):
        try:
            student = md.StudentAssignment.objects.get(
                student=self.context['request'].user, assignment=obj)
            serializer = StudentAssignmentSerializer(student)
            return serializer.data
        except md.StudentAssignment.DoesNotExist:
            return None

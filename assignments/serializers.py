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

#
# class StringSerializer(sz.StringRelatedField):
#     def to_internal_value(self, value):
#         return value
#
#
# class QuestionSerializer(sz.ModelSerializer):
#     class Meta:
#         model = md.Question
#         fields = ('id', 'choices', 'title', 'order')
#     choices = StringSerializer(many=True)
#
#
# class MyQQSerializer(sz.ModelSerializer):
#     class Meta:
#         model = md.Question
#         fields = '__all__'
#
#
#
# class AnswerSerializer(sz.ModelSerializer):
#     class Meta:
#         model = md.Answer
#         fields = ('id', 'student', 'answered_question',
#                   'answer_choice', 'answer_text')
#
#
# class AssignmentSerializer(sz.ModelSerializer):
#     questions = sz.SerializerMethodField()
#     teacher = StringSerializer(many=False)
#
#     class Meta:
#         model = md.Assignment
#         fields = '__all__'
#
#     def get_questions(self, obj):
#         questions = QuestionSerializer(obj.questions.all(), many=True).data
#         return questions
#
#     def create(self, request):
#         data = request.data
#
#         assignment = md.Assignment()
#         teacher = User.objects.get(username=data['teacher'])
#         assignment.teacher = teacher
#         assignment.title = data['title']
#         assignment.save()
#
#         order = 1
#         for q in data['questions']:
#             newQ = md.Question()
#             newQ.title = q['title']
#             newQ.text = q['text']
#             newQ.order = order
#             newQ.save()
#
#             if newQ.type in [1, 2]:
#                 for c in q['choices']:
#                     newC = md.Choice()
#                     newC.title = c
#                     newC.save()
#                     newQ.choices.add(newC)
#
#             newQ.assignment = assignment
#             newQ.save()
#             order += 1
#         return assignment
#
#
# class QuestionAnswersSerializer(sz.ModelSerializer):
#     class Meta:
#         model = md.Question
#         fields = '__all__'
#     answers = sz.SerializerMethodField()
#
#     def get_answers(self, obj):
#         answers = AnswerSerializer(obj.answers.all(), many=True).data
#         return answers
#
#
# class GradedAssignmentSerializer(sz.ModelSerializer):
#     student = StringSerializer(many=False)
#
#     class Meta:
#         model = md.GradedAssignment
#         fields = '__all__'
#
#     def create(self, request):
#         data = request.data
#
#         assignment = md.Assignment.objects.get(id=data['asntId'])
#         student = User.objects.get(username=data['username'])
#
#         graded_asnt = md.GradedAssignment()
#         graded_asnt.assignment = assignment
#         graded_asnt.student = student
#
#         questions = [q for q in assignment.questions.all()]
#         answers = [data['answers'][a] for a in data['answers']]
#
#         answered_correct_count = 0
#         for i in range(len(questions)):
#             if questions[i].answer.title == answers[i]:
#                 answered_correct_count += 1
#             i += 1
#
#         grade = answered_correct_count / len(questions) * 100
#         graded_asnt.grade = grade
#         graded_asnt.save()
#         return graded_asnt

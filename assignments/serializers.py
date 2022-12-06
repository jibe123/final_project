from rest_framework import serializers as sz

from accounts.models import User, Student
import assignments.models as md


class StringSerializer(sz.StringRelatedField):
    def to_internal_value(self, value):
        return value


class QuestionSerializer(sz.ModelSerializer):
    class Meta:
        model = md.Question
        fields = ('id', 'choices', 'title', 'order')
    choices = StringSerializer(many=True)


class AnswerSerializer(sz.ModelSerializer):
    class Meta:
        model = md.Answer
        fields = ('id', 'student', 'answered_question',
                  'answer_choice', 'answer_text')


class AssignmentSerializer(sz.ModelSerializer):
    questions = sz.SerializerMethodField()
    teacher = StringSerializer(many=False)

    class Meta:
        model = md.Assignment
        fields = '__all__'

    def get_questions(self, obj):
        questions = QuestionSerializer(obj.questions.all(), many=True).data
        return questions

    def create(self, request):
        data = request.data

        assignment = md.Assignment()
        teacher = User.objects.get(username=data['teacher'])
        assignment.teacher = teacher
        assignment.title = data['title']
        assignment.save()

        order = 1
        for q in data['questions']:
            newQ = md.Question()
            newQ.title = q['title']
            newQ.text = q['text']
            newQ.order = order
            newQ.save()

            if newQ.type in [1, 2]:
                for c in q['choices']:
                    newC = md.Choice()
                    newC.title = c
                    newC.save()
                    newQ.choices.add(newC)

            newQ.assignment = assignment
            newQ.save()
            order += 1
        return assignment


class QuestionAnswersSerializer(sz.ModelSerializer):
    class Meta:
        model = md.Question
        fields = '__all__'
    answers = sz.SerializerMethodField()

    def get_answers(self, obj):
        answers = AnswerSerializer(obj.answers.all(), many=True).data
        return answers


class GradedAssignmentSerializer(sz.ModelSerializer):
    student = StringSerializer(many=False)

    class Meta:
        model = md.GradedAssignment
        fields = '__all__'

    def create(self, request):
        data = request.data

        assignment = md.Assignment.objects.get(id=data['asntId'])
        student = User.objects.get(username=data['username'])

        graded_asnt = md.GradedAssignment()
        graded_asnt.assignment = assignment
        graded_asnt.student = student

        questions = [q for q in assignment.questions.all()]
        answers = [data['answers'][a] for a in data['answers']]

        answered_correct_count = 0
        for i in range(len(questions)):
            if questions[i].answer.title == answers[i]:
                answered_correct_count += 1
            i += 1

        grade = answered_correct_count / len(questions) * 100
        graded_asnt.grade = grade
        graded_asnt.save()
        return graded_asnt

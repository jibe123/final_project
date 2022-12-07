from django.contrib import admin
import nested_admin
from .models import (Assignment, Question, Choice,
                     StudentAssignment, Answer)


class ChoiceInline(nested_admin.NestedTabularInline):
    model = Choice
    extra = 4
    max_num = 4


class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [ChoiceInline, ]
    extra = 5


class AssignmentAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline, ]


class AnswerInline(admin.TabularInline):
    model = Answer


class StudentAssignmentAdmin(admin.ModelAdmin):
    inlines = [AnswerInline, ]


admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(StudentAssignment, StudentAssignmentAdmin)
admin.site.register(Answer)

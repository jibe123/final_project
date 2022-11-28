from django.db import models

from accounts.models import User
from timetable.models import Course


class Assignment(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assignments",
        limit_choices_to={'is_teacher': True}, verbose_name="Преподаватель")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="assignments",
        verbose_name="Курс")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


class GradedAssignment(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={'is_student': True}, verbose_name="Студент")
    assignment = models.ForeignKey(
        Assignment, on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name="Задание")
    grade = models.FloatField(verbose_name="Оценка")

    def __str__(self):
        return self.student.username

    class Meta:
        verbose_name = "Оцененное задание"
        verbose_name_plural = "Оцененные задания"


class Choice(models.Model):
    title = models.CharField(max_length=50,
                             verbose_name="Название варианта")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Вариант"
        verbose_name_plural = "Варианты"


class Question(models.Model):
    question = models.CharField(max_length=200, verbose_name="Вопрос")
    choices = models.ManyToManyField(Choice, verbose_name="Варианты")
    answer = models.ForeignKey(
        Choice, on_delete=models.CASCADE, related_name='answer',
        blank=True, null=True, verbose_name="Ответ")
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='questions',
        blank=True, null=True, verbose_name="Задание")
    order = models.SmallIntegerField(verbose_name="Порядковый номер")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
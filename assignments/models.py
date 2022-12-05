from django.db import models

from accounts.models import User, Student
from timetable.models import Course


TYPES = (
        (1, 'Один правильный вариант'),
        (2, 'Несколько правильных вариантов'),
        (3, 'Текстовый ответ')
    )


class Assignment(models.Model):
    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    title = models.CharField(max_length=255, verbose_name="Название")
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assignments",
        limit_choices_to={'is_teacher': True}, verbose_name="Преподаватель")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="assignments",
        verbose_name="Курс")

    def __str__(self):
        return self.title


class GradedAssignment(models.Model):
    class Meta:
        verbose_name = "Оцененное задание"
        verbose_name_plural = "Оцененные задания"

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, verbose_name="Студент")
    assignment = models.ForeignKey(
        Assignment, on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name="Задание")
    grade = models.FloatField(verbose_name="Оценка")

    def __str__(self):
        return f"{self.student} - {self.assignment}"


class Question(models.Model):
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    title = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Вопрос")
    type = models.PositiveSmallIntegerField(
        choices=TYPES, default=1, verbose_name="Тип вопроса")
    text = models.CharField(max_length=2000, verbose_name='Текст вопроса')
    assignment = models.ForeignKey(
        Assignment, on_delete=models.DO_NOTHING, related_name='questions',
        blank=True, null=True, verbose_name="Задание")
    order = models.SmallIntegerField(verbose_name="Порядковый номер вопроса")

    def __str__(self):
        return self.title


class Choice(models.Model):
    class Meta:
        verbose_name = "Вариант"
        verbose_name_plural = "Варианты"

    question = models.ForeignKey(
        Question, on_delete=models.DO_NOTHING, related_name='choices',
        blank=True, null=True, verbose_name="Вопрос")
    title = models.CharField(max_length=255,
                            verbose_name="Текст варианта")
    is_correct = models.BooleanField(default=False,
                                     verbose_name="Правильный вариант?")

    def __str__(self):
        return self.title


class Answer(models.Model):
    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                verbose_name='Студент')
    answered_question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                          verbose_name='Ответ на вопрос')
    answer_choice = models.ForeignKey(Choice, on_delete=models.CASCADE,
                                      null=True, blank=True,
                                      verbose_name='Выбранный вариант')
    answer_text = models.CharField(max_length=2000, null=True, blank=True,
                                   verbose_name='Текст ответа')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Время сдачи')

    def __str__(self):
        return f'{self.student} - {self.answered_question} - ' \
               f'{self.answer_choice or ""}{self.answer_text or ""}'

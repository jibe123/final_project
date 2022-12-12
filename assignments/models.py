from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from accounts.models import User, Student
from timetable.models import Course


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
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='questions',
        blank=True, null=True, verbose_name="Задание")
    text = models.CharField(
        max_length=2000, verbose_name="Текст вопроса")
    order = models.SmallIntegerField(verbose_name="Порядковый номер вопроса")

    def __str__(self):
        return self.text


class Choice(models.Model):
    class Meta:
        verbose_name = "Вариант"
        verbose_name_plural = "Варианты"

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='choices',
        blank=True, null=True, verbose_name="Вопрос")
    text = models.CharField(
        max_length=255, verbose_name="Текст варианта")
    is_correct = models.BooleanField(default=False,
                                     verbose_name="Правильный вариант?")

    def __str__(self):
        return self.text


class StudentAssignment(models.Model):
    class Meta:
        verbose_name = "Выполненное задание"
        verbose_name_plural = "Выполненные задания"
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='st_assignments',
        verbose_name='Студент')
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='st_assignments',
        blank=True, null=True, verbose_name="Задание")
    grade = models.FloatField(default=0, verbose_name="Оценка")
    completed = models.BooleanField(
        default=False, verbose_name="Выполнено?")
    date_completed = models.DateTimeField(
        null=True, auto_now_add=True, verbose_name="Дата сдачи")
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    graded = models.BooleanField(default=False)

    def __str__(self):
        return self.student.user.username


class Answer(models.Model):
    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    student = models.ForeignKey(
        StudentAssignment, on_delete=models.CASCADE, related_name='answers',
        verbose_name='Студент')
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers',
        verbose_name='Ответ на вопрос')
    choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE, null=True, blank=True,
        related_name='answers', verbose_name='Выбранный вариант')
    answer_text = models.CharField(
        max_length=2000, null=True, blank=True,
        verbose_name='Текст ответа')

    def __str__(self):
        return self.question.text


@receiver(pre_save, sender=Assignment)
def slugify_title(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title, allow_unicode=True)

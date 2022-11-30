import datetime
from django.db import models

from accounts.models import User, Group


class Course(models.Model):
    title = models.CharField(
        max_length=255, verbose_name="Название курса")
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="courses",
        limit_choices_to={'is_teacher': True}, verbose_name="Преподаватель")
    duration = models.DurationField(
        default=datetime.timedelta(hours=1, minutes=20),
        verbose_name="Продолжительность занятий")
    groups = models.ManyToManyField(Group, related_name="courses")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class CourseMaterials(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс",
        related_name="materials")
    caption = models.CharField(
        max_length=500, null=True, blank=True,
        verbose_name="Описание")
    file = models.FileField(
        upload_to='materials/', null=True, blank=True,
        verbose_name="Материал")
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Материал по курсу"
        verbose_name_plural = "Материалы по курсу"


class TableDay(models.Model):
    class Day(models.IntegerChoices):
        MON = 1, "Понедельник"
        TUE = 2, "Вторник"
        WED = 3, "Среда"
        THU = 4, "Четверг"
        FRI = 5, "Пятница"
        SAT = 6, "Суббота"

    day = models.PositiveSmallIntegerField(
        choices=Day.choices, default=Day.MON, verbose_name="День недели")

    def __str__(self):
        return self.get_day_display()

    class Meta:
        verbose_name = "День в расписании"
        verbose_name_plural = "Дни в расписании"


class CourseDay(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course_days",
        verbose_name="Курс")
    table_day = models.ForeignKey(
        TableDay, on_delete=models.CASCADE, related_name="table_days",
        verbose_name="День в расписании")
    start_time = models.TimeField(
        blank=True, null=True, verbose_name="Время начала занятий")

    def __str__(self):
        return f"{self.course} в {self.table_day.get_day_display()} в {self.start_time}"

    class Meta:
        verbose_name = "Расписание курса"
        verbose_name_plural = "Расписание курсов"

import datetime
from django.db import models

from accounts.models import User


class Course(models.Model):
    title = models.CharField(
        max_length=255, verbose_name="Название курса")
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="courses",
        limit_choices_to={'is_teacher': True}, verbose_name="Преподаватель")
    duration = models.DurationField(
        default=datetime.timedelta(hours=1, minutes=20),
        verbose_name="Продолжительность занятий")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class TableDay(models.Model):
    class Day(models.IntegerChoices):
        MON = 1, "MONDAY"
        TUE = 2, "TUESDAY"
        WED = 3, "WEDNESDAY"
        THU = 4, "THURSDAY"
        FRI = 5, "FRIDAY"
        SAT = 6, "SATURDAY"

    day = models.PositiveSmallIntegerField(
        choices=Day.choices, default=Day.MON, verbose_name="День недели")

    def __str__(self):
        return self.Day.name

    class Meta:
        verbose_name = "День в расписании"
        verbose_name_plural = "Дни в расписании"


class CourseDay(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course_days",
        verbose_name="Курс")
    table_day = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="table_days",
        verbose_name="День в расписании")
    start_time = models.TimeField(
        blank=True, null=True, verbose_name="Время начала занятий")

    def __str__(self):
        return f"{self.course} on {self.table_day} at {self.start_time}"

    class Meta:
        verbose_name = "Расписание курса"
        verbose_name_plural = "Расписание курсов"

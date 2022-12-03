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


class Weekdays(models.Model):
    class Day(models.IntegerChoices):
        MON = 1, "Понедельник"
        TUE = 2, "Вторник"
        WED = 3, "Среда"
        THU = 4, "Четверг"
        FRI = 5, "Пятница"
        SAT = 6, "Суббота"

    day = models.PositiveSmallIntegerField(
        primary_key=True, choices=Day.choices,
        default=Day.MON, verbose_name="День недели")

    def __str__(self):
        return self.get_day_display()

    class Meta:
        verbose_name = "День недели"
        verbose_name_plural = "Дни недели"


class StartTimes(models.Model):
    START_TIME_CHOICES = (
        (1, "08:00"),
        (2, "09:30"),
        (3, "11:00"),
        (4, "13:00"),
        (5, "14:30"),
        (6, "16:00"),
        (7, "17:30"),
    )
    start_time = models.PositiveSmallIntegerField(
        primary_key=True, choices=START_TIME_CHOICES,
        default=1, verbose_name="Время начала")

    def __str__(self):
        return self.get_start_time_display()

    class Meta:
        verbose_name = "Время начала в расписании"
        verbose_name_plural = "Времена начала в расписании"


class Timetable(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course_days",
        verbose_name="Курс")
    weekday = models.ForeignKey(
        Weekdays, on_delete=models.CASCADE, related_name="weekdays",
        verbose_name="День недели")
    start_time = models.ForeignKey(
        StartTimes, on_delete=models.CASCADE, related_name='start_times',
        verbose_name="Время начала занятий")

    def __str__(self):
        return f"{self.course} в {self.weekday.get_day_display()}" \
               f" в {self.start_time.get_start_time_display()}"

    class Meta:
        verbose_name = "Расписание курса"
        verbose_name_plural = "Расписание курсов"
        unique_together = ('course', 'weekday', 'start_time',)

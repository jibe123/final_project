from django.contrib import admin

from .models import Course, Weekdays, StartTimes, Timetable

admin.site.register(Course)
admin.site.register(Weekdays)
admin.site.register(StartTimes)
admin.site.register(Timetable)

from django.contrib import admin

from .models import Course, TableDay, CourseDay

admin.site.register(Course)
admin.site.register(TableDay)
admin.site.register(CourseDay)

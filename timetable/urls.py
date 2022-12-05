from django.urls import path, include
from rest_framework.routers import DefaultRouter

import timetable.views as vs

router = DefaultRouter()

router.register('timetable', vs.TimetableViewSet)
router.register('courses', vs.CourseViewSet, basename='courses')
router.register('materials', vs.CourseMaterialsViewSet, basename='materials')

urlpatterns = [
    path('', include(router.urls)),
]

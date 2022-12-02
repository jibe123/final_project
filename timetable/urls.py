from django.urls import path, include
from rest_framework.routers import DefaultRouter

import timetable.views as vs

router = DefaultRouter()

router.register(r'timetable', vs.TimetableViewSet)
router.register(r'courses', vs.CourseViewSet)
router.register(r'upload_materials', vs.CourseMaterialsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

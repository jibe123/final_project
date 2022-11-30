from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import update_groups_data, TimetableViewSet, CourseViewSet

router = DefaultRouter()
router_courses = DefaultRouter()

router.register("timetable", TimetableViewSet)
router_courses.register("upload_materials", CourseViewSet)

urlpatterns = [
    path('update_groups/', update_groups_data, name='update-groups'),
    path('', include(router_courses.urls)),
    path('', include(router.urls)),
]

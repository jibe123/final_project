from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    update_groups_data,
    TimetableViewSet,
    CourseViewSet,
    CourseMaterialsViewSet)

router = DefaultRouter()
router2 = DefaultRouter()
router3 = DefaultRouter()

router.register("timetable", TimetableViewSet)
router2.register("upload_materials", CourseMaterialsViewSet)
router3.register("courses", CourseViewSet)

urlpatterns = [
    path('update_groups/', update_groups_data, name='update-groups'),
    path('', include(router2.urls)),
    path('', include(router.urls)),
    path('', include(router3.urls)),
]

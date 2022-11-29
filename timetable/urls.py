from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import update_groups_data, TimetableViewSet

router = DefaultRouter()
router.register("timetable", TimetableViewSet)

urlpatterns = [
    path('update_groups/', update_groups_data, name='update-groups'),
    path('', include(router.urls)),
]

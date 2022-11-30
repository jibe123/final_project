from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import (
    StudentCreateAPIView,
    UserViewSet,
    PermissionViewSet,
    StudentViewSet)

router = DefaultRouter()
router2 = DefaultRouter()
router3 = DefaultRouter()
router.register('users', UserViewSet)
router2.register('permissions', PermissionViewSet)
router3.register('students', StudentViewSet)


urlpatterns = [
    path('add_students/', StudentCreateAPIView.as_view(), name='add_students_view'),
    path('', include(router.urls)),
    path('', include(router2.urls)),
    path('', include(router3.urls)),
]
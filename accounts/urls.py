from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import (
    StudentCreateAPIView,
    UserViewSet,
    PermissionViewSet,
    StudentViewSet,
    GroupViewSet)

router = DefaultRouter()

# router.register('users', UserViewSet)
# router.register('permissions', PermissionViewSet)
router.register('students', StudentViewSet)
router.register('groups', GroupViewSet)


urlpatterns = [
    path('add_students/', StudentCreateAPIView.as_view(), name='add_students_view'),
    path('', include(router.urls)),
]

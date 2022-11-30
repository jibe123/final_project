from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import StudentCreateAPIView, UserViewSet, PermissionViewSet

router = DefaultRouter()
router2 = DefaultRouter()
router.register('users', UserViewSet)
router2.register('permissions', PermissionViewSet)


urlpatterns = [
    path('add_students/', StudentCreateAPIView.as_view(), name='add_students_view'),
    path('', include(router.urls)),
    path('', include(router2.urls)),
]
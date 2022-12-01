from django.urls import path, include
from rest_framework.routers import DefaultRouter

import accounts.views as vs

router = DefaultRouter()

router.register('students', vs.StudentViewSet)
router.register('groups', vs.GroupViewSet)


urlpatterns = [
    path('students/create/', vs.StudentCreateAPIView.as_view(),
         name='students-create'),
    path('', include(router.urls)),
]

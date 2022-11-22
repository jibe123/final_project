from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .models import News
from .views import NewsViewSet

router = DefaultRouter()
router.register("news", NewsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

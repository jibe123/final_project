from django.urls import path, include
from rest_framework.routers import DefaultRouter
from board import views

router = DefaultRouter()
router.register(r'threads', views.ThreadViewSet)
router.register(r'messages', views.MessageViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

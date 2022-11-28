from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    AssignmentViewSet,
    GradedAssignmentListView,
    GradedAssignmentCreateView)

router = DefaultRouter()

router.register(r'', AssignmentViewSet)
urlpatterns = [
    path('', router.urls),
    path('graded/', GradedAssignmentListView.as_view()),
    path('create/', GradedAssignmentCreateView.as_view())
]

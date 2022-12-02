from django.urls import path, include
from rest_framework.routers import DefaultRouter

import assignments.views as vs

router = DefaultRouter()

router.register(r'', vs.AssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('graded/', vs.GradedAssignmentListView.as_view()),
    path('create/', vs.GradedAssignmentCreateView.as_view())
]

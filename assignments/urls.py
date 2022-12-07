from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

import assignments.views as vs

urlpatterns = [
    path('my-quizzes/', vs.MyAssignmentListAPI.as_view()),
    path('quizzes/', vs.AssignmentListAPI.as_view()),
    re_path(r'quizzes/(?P<slug>[\w\-]+)/$', vs.AssignmentDetailAPI.as_view()),
    re_path(r'quizzes/(?P<slug>[\w\-]+)/save-answer/$', vs.SaveAnswer.as_view()),
    re_path(r'quizzes/(?P<slug>[\w\-]+)/submit/$', vs.SubmitAssignmentAPI.as_view()),
]

# router = DefaultRouter()
#
# router.register('assignments', vs.AssignmentViewSet, basename='assignments')
# router.register('questions', vs.QQViewSet, basename='qq')

# urlpatterns = [
#     path('', include(router.urls)),
# path('assignments_graded/', vs.GradedAssignmentListView.as_view()),
# path('assignments_grade/', vs.GradedAssignmentCreateView.as_view()),

# ]

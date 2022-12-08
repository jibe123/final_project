from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

import assignments.views as vs


urlpatterns = [
    path('my-assignments/', vs.MyAssignmentListAPI.as_view()),
    path('assignments/', vs.AssignmentListAPI.as_view()),
    re_path(r'assignments/(?P<slug>[\w\-]+)/$', vs.AssignmentDetailAPI.as_view()),
    re_path(r'assignments/(?P<slug>[\w\-]+)/(?P<pk>\d+)/$', vs.SaveAnswer.as_view()),
    re_path(r'assignments/(?P<slug>[\w\-]+)/submit/$', vs.SubmitAssignmentAPI.as_view()),
]

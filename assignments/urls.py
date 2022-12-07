from django.urls import path, re_path
import assignments.views as vs

urlpatterns = [
    path('my-quizzes/', vs.MyAssignmentListAPI.as_view()),
    path('quizzes/', vs.AssignmentListAPI.as_view()),
    re_path(r'quizzes/(?P<slug>[\w\-]+)/$', vs.AssignmentDetailAPI.as_view()),
    re_path(r'quizzes/(?P<slug>[\w\-]+)/save-answer/$', vs.SaveAnswer.as_view()),
    re_path(r'quizzes/(?P<slug>[\w\-]+)/submit/$', vs.SubmitAssignmentAPI.as_view()),
]

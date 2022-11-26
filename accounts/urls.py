from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import StudentCreateAPIView


urlpatterns = [
    path('add_students/', StudentCreateAPIView.as_view(), name='add_students_view'),
    path('authentication/', include('rest_framework.urls')),
]
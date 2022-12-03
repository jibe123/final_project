from django.urls import path, include
from django.contrib.auth.views import LoginView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

import authusers.views as vs

urlpatterns = [
    path('token/', vs.MyTokenObtainPairView.as_view(
        template_name="authusers/login.html"), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('login/', LoginView.as_view(
        template_name="authusers/login.html"), name='login'),
    path('password_reset/', include(
        'django_rest_passwordreset.urls',
        namespace='password_reset')),
    path('change_password/', vs.ChangePasswordView.as_view(),
         name='change-password'),
    path('change_profile_photo/', vs.ChangeProfilePhotoView.as_view(),
         name='change-profile-photo'),
]

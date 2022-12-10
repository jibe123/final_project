from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

import authusers.views as vs

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('password_reset/', include(
        'django_rest_passwordreset.urls',
        namespace='password_reset')),
    path('change_password/', vs.ChangePasswordView.as_view(),
         name='change-password'),
    path('change_profile_photo/', vs.ChangeProfilePhotoView.as_view(),
         name='change-profile-photo'),
    path('login/', LoginView.as_view(
        template_name='admin/login.html'), name='login'),
    path('logout/', LogoutView.as_view(
        template_name='admin/logout.html'), name='logout'),
]

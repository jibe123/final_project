from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

import authusers.views as vs

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(),
         name='login'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('password_reset/', include(
        'django_rest_passwordreset.urls',
        namespace='password_reset')),
    path('change_password/', vs.ChangePasswordView.as_view(),
         name='change-password'),
    path('change_profile_photo/', vs.ChangeProfilePhotoView.as_view(),
         name='change-profile-photo'),
]

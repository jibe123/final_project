from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import (MyObtainTokenPairView,
                            StudentCreateAPIView,
                            UserListAPIView)


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('add_students/', StudentCreateAPIView.as_view(), name='add_students_view'),
    path('users_list/', UserListAPIView.as_view(), name='users_list'),
    path('authentication/', include('rest_framework.urls')),
]
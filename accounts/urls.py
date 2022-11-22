from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import MyObtainTokenPairView, UserCreateAPIView, UserListAPIView


urlpatterns = [
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/add/', UserCreateAPIView.as_view(), name='add_users_view'),
    path('users/list/', UserListAPIView.as_view(), name='users_list'),
]
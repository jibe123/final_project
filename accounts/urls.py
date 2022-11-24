from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import (MyObtainTokenPairView,
                            UserCreateAPIView,
                            UserListAPIView,
                            set_student_groups,
                            set_officer_department)


urlpatterns = [
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/add/', UserCreateAPIView.as_view(), name='add_users_view'),
    path('add_students_to_group/', set_student_groups, name='set_group_view'),
    path('add_officers_to_department/', set_officer_department, name='set_department_view'),
    path('users/list/', UserListAPIView.as_view(), name='users_list'),
]
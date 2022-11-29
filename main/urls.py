from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('news.urls')),
    path('api/v1/auth/', include('authusers.urls')),
    path('api/v1/data/', include('accounts.urls')),
    path('api/v1/board/', include('board.urls')),
    path('api/v1/', include('timetable.urls')),
]

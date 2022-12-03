from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/data/', include('accounts.urls')),
    path('api/v1/assignments/', include('assignments.urls')),
    path('api/v1/auth/', include('authusers.urls')),
    path('api/v1/board/', include('board.urls')),
    path('api/v1/news/', include('news.urls'), name='news'),
    path('api/v1/study/', include('timetable.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

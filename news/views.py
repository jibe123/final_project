from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .serializers import NewsSerializer
from .models import News
from .permissions import IsSuperuser, IsOwner, IsManager


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsSuperuser | IsManager]

        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsSuperuser | IsOwner]

        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

from rest_framework import permissions as ps, viewsets

from accounts.models import User
from accounts.permissions import IsSuperuser
from .permissions import IsOwnerOrReadOnly
from .models import Thread, Message
import board.serializers as msz


class MessageViewSet(viewsets.ModelViewSet):

    queryset = Message.objects.all()
    serializer_class = msz.MessageSerializer
    permission_classes = [ps.IsAuthenticatedOrReadOnly |
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = msz.ThreadSerializer
    permission_classes = [ps.IsAuthenticatedOrReadOnly |
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = msz.UserSerializer
    permission_classes = [IsSuperuser]

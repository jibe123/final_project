from rest_framework import serializers as sz

from accounts.models import User
from .models import Thread, Message


class UserSerializer(sz.HyperlinkedModelSerializer):
    threads = sz.HyperlinkedRelatedField(
        many=True, view_name='thread-detail',
        queryset=Thread.objects.all(), required=False)
    messages = sz.HyperlinkedRelatedField(
        many=True, view_name='message-detail',
        queryset=Message.objects.all(), required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'threads', 'messages')


class MessageSerializer(sz.HyperlinkedModelSerializer):
    owner = sz.ReadOnlyField(source='owner.username')
    thread = sz.HyperlinkedRelatedField(
        many=False, view_name='thread-detail',
        queryset=Thread.objects.all(), required=False)
    likes = sz.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all())

    def update(self, instance, validated_data):
        likes = validated_data.pop('likes')
        for i in likes:
            instance.likes.add(i)
        instance.save()
        return instance

    class Meta:
        model = Message
        fields = ('id', 'title', 'body_text', 'owner', 'likes', 'thread')


class ThreadSerializer(sz.HyperlinkedModelSerializer):
    owner = sz.ReadOnlyField(source='owner.username')
    messages = sz.HyperlinkedRelatedField(
        many=True, view_name='message-detail',
        queryset=Message.objects.all())

    class Meta:
        model = Thread
        fields = ('id', 'title', 'owner', 'messages')

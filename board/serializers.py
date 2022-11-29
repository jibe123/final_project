from rest_framework import serializers

from accounts.models import User
from .models import Thread, Message


class UserSerializer(serializers.HyperlinkedModelSerializer):
    threads = serializers.HyperlinkedRelatedField(
        many=True, view_name='thread-detail',
        queryset=Thread.objects.all(), required=False)
    messages = serializers.HyperlinkedRelatedField(
        many=True, view_name='message-detail',
        queryset=Message.objects.all(), required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'threads', 'messages')


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    thread = serializers.HyperlinkedRelatedField(
        many=False, view_name='thread-detail',
        queryset=Thread.objects.all(), required=False)
    likes = serializers.PrimaryKeyRelatedField(
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


class ThreadSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    messages = serializers.HyperlinkedRelatedField(
        many=True, view_name='message-detail',
        queryset=Message.objects.all())

    class Meta:
        model = Thread
        fields = ('id', 'title', 'owner', 'messages')

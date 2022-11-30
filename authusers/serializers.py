from rest_framework import serializers

from accounts.models import User


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ChangeProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_image',)

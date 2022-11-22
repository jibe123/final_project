import secrets

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        return token


class NewUserSerializer(serializers.ModelSerializer):
    user_must_change_password = serializers.HiddenField(default=True)
    is_management = serializers.BooleanField(default=False)
    is_officer = serializers.BooleanField(default=False)
    is_student = serializers.BooleanField(default=False)
    password = serializers.CharField(write_only=True, default="")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'user_must_change_password',
                  'is_management', 'is_officer', 'is_teacher', 'is_student',
                  'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            username="temporary_username",
            user_must_change_password=validated_data.get("user_must_change_password"),
            is_management=validated_data.get("is_management"),
            is_officer=validated_data.get("is_officer"),
            is_teacher=validated_data.get("is_teacher"),
            is_student=validated_data.get("is_student")
        )
        allowed_chars = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        length = 11
        password = "".join(secrets.choice(allowed_chars) for i in range(length))
        user.set_password(password)
        user.check_password(password)
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

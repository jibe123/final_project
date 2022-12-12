from rest_framework import serializers as sz

from accounts.models import User


class ChangePasswordSerializer(sz.Serializer):
    old_password = sz.CharField(required=True)
    new_password = sz.CharField(required=True)
    new_password2 = sz.CharField(required=True)

    def validate(self, data):
        if data['new_password'] and data['new_password2'] \
                and data['new_password'] != data['new_password2']:
            raise sz.ValidationError(
                "Пароли не совпадают!"
            )
        return data


class ChangeUserProfileSerializer(sz.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'user_image', 'first_name', 'last_name', 'email')

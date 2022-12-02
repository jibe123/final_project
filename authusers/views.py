from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.signals import reset_password_token_created

from accounts.models import User
import authusers.serializers as msz


@receiver(post_save, sender=User)
def reset_password(sender, instance, created, *args, **kwargs):
    if created:
        if instance.auto_password:
            token = ResetPasswordToken.objects.create(user=instance)
            send_mail(
                "Сброс пароля",
                f'''
                Это ваш токен для сброса пароля.
                Токен: {token.key}
                Перейдите по ссылке, введите ваш токен и новый пароль.
                http://127.0.0.1:8000/api/v1/auth/password_reset/confirm/''',
                "jibek.k@gmail.com",
                [instance.email]
            )


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token,
                                 *args, **kwargs):
    email_plaintext_message = reset_password_token.key

    send_mail(
        "Восстановление пароля",
        f'''
        Это ваш токен для восстановления пароля
        Токен: {email_plaintext_message}. 
        Перейдите по ссылке, введите ваш токен и новый пароль
        http://127.0.0.1:8000/api/v1/auth/password_reset/confirm/''',
        "jibek.k@gmail.com",
        [reset_password_token.user.email]
    )


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = msz.ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not obj.check_password(
                    serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            obj.set_password(serializer.data.get("new_password"))
            obj.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeProfilePhotoView(APIView):
    parser_classes = (MultiPartParser, FormParser,)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = msz.ChangeProfilePhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

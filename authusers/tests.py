from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


class AuthUsersTest(APITestCase):

    def setUp(self):
        User.objects.create_user(
            username='john',
            email='js@js.com',
            password='js.sj',
            is_manager=True)

    @property
    def bearer_token(self):
        user = User.objects.last()
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}

    def test_get_access(self):
        url = reverse('students-create')
        response = self.client.get(url, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_access(self):
        url = reverse('students-create')
        data = {"first_name": "QQQ",
                "last_name": "ZZZ",
                "email": "qqq@zzz.com"}
        response = self.client.post(url, data, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.last().username, "qqq.zzz")

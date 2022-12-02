from django.test import Client
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from .models import News


class NewsTest(APITestCase):
    def setUp(self):
        self.client = Client()

        self.manager = User(username='manager', is_manager=True)
        self.manager.set_password('manager')
        self.manager.save()

        self.manager2 = User(username='manager2', is_manager=True)
        self.manager2.set_password('manager2')
        self.manager2.save()

    def test_get_news(self):
        url = 'http://127.0.0.1:8000/api/v1/news/'
        response = self.client.get(url)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_news_post_permission(self):
        url = 'http://127.0.0.1:8000/api/v1/news/'
        data = {"name": "QQQQQQQQQQQQ",
                "news_text": "RRRRRRRRRRRRRRRR"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_post_news(self):
        self.client.login(username='manager', password='manager')
        url = 'http://127.0.0.1:8000/api/v1/news/'
        data = {"name": "ABCZ",
                "news_text": "RRRRRRRRRRRRRRRR"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)
        news = News.objects.last()
        self.assertEqual(news.name, "ABCZ")

    def test_news_check_owner_permission(self):
        self.client.login(username='manager2', password='manager2')
        url = 'http://127.0.0.1:8000/api/v1/news/'
        data = {"name": "YYYYY",
                "news_text": "EEEE"}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)
        news = News.objects.last()
        self.assertEqual(news.news_text, "EEEE")

        news = News.objects.last()
        url = f'http://127.0.0.1:8000/api/v1/news/{news.pk}/'
        data = {"name": "TTT",
                "news_text": "MMM"}
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        news = News.objects.last()
        self.assertEqual(news.name, "TTT")

        news = News.objects.last()
        url = f'http://127.0.0.1:8000/api/v1/news/{news.pk}/'
        self.client.login(username='manager', password='manager')
        response = self.client.delete(url)
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

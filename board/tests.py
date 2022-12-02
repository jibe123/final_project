from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from accounts.models import User
from board.models import Message, Thread
from .serializers import ThreadSerializer, MessageSerializer


class BoardTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin', password='admin')
        self.client.login(username='admin', password='admin')
        self.user = User.objects.create(
            username='the_user', password='the_user')
        self.thread = Thread.objects.create(
            title="the_thread", owner=self.superuser)
        self.message = Message.objects.create(owner=self.superuser,
                                              title="The message",
                                              thread=self.thread,
                                              body_text="Body text")

    def test_can_read_user_list(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_user_detail(self):
        response = self.client.get(reverse('user-detail',
                                           args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_create_thread(self):
        self.data = {"title": "The Test Thread 1", "messages": []}
        response = self.client.post(reverse('thread-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_read_thread_list(self):
        response = self.client.get(reverse('thread-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_thread_detail(self):
        response = self.client.get(reverse('thread-detail',
                                           args=[self.thread.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_update_thread(self):
        factory = APIRequestFactory()
        request = factory.get('/')
        self.data = ThreadSerializer(
            self.thread, context={'request': request}).data
        self.data.update({'title': 'Changed'})
        response = self.client.put(reverse('thread-detail',
                                           args=[self.thread.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_delete_thread(self):
        response = self.client.delete(reverse('thread-detail',
                                              args=[self.thread.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_create_message(self):
        factory = APIRequestFactory()
        request = factory.get('/')
        self.threadData = ThreadSerializer(
            self.thread, context={'request': request}).data
        self.data = {"title": "Test Message",
                     'thread': reverse('thread-detail',
                                       args=[self.thread.id]),
                     "body_text":
                         """
                         ZZZZZZZZZZZZZZ
                         WWWWWWWWWWWWWWWWWWWWWWW
                         IIIIIIIIIIIIIIIIIIIIIIIII
                         QQQQQQQQQQQQQQQQQ
                         """
                     }
        response = self.client.post(reverse('message-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_read_message_list(self):
        response = self.client.get(reverse('message-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_message_detail(self):
        response = self.client.get(reverse('message-detail',
                                           args=[self.message.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_update_message(self):
        factory = APIRequestFactory()
        request = factory.get('/')
        self.data = MessageSerializer(
            self.message, context={'request': request}).data
        self.data.update({'title': 'Changed'})
        response = self.client.put(reverse('thread-detail',
                                           args=[self.message.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_delete_message(self):
        response = self.client.delete(reverse('message-detail',
                                              args=[self.message.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

import factory

from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User, Student, Group


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student
    group = factory.Iterator(Group.objects.all())


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    is_student = True

    class Params:
        generate_account = factory.Trait(
            student=factory.RelatedFactory(
                StudentFactory, factory_related_name='user_id')
        )


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group
    name = factory.Faker("name")


class AccountsTest(APITestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username='admin', password='admin')
        self.client.login(username='admin', password='admin')
        UserFactory.create_batch(50)
        GroupFactory.create_batch(5)

    def test_login(self):
        response = self.client.get('/admin/', follow=True)
        login_response = self.client.login(
            username='admin', password='admin')
        self.assertTrue(response)
        self.assertTrue(login_response)

    def test_objects_count(self):
        self.assertEqual(User.objects.all().count(), 51)
        self.assertEqual(Group.objects.all().count(), 5)
        self.assertEqual(Student.objects.all().count(), 50)

    def test_create_students(self):
        url = reverse('students-create')
        data = {"first_name": "QWERTY",
                "last_name": "QWERTY",
                "email": "qwerty@qwerty.qw"}
        response = self.client.post(url, data, format='json')
        created_user = User.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created_user.username, "qwerty.qwerty")

    def test_assign_group(self):
        url = 'https://127.0.0.1:8000/api/v1/data/groups/'
        created_user = User.objects.last().pk
        data = {"name": "ABC",
                "students": created_user}
        response = self.client.post(url, data, format='json')
        created_group = Group.objects.last()
        created_student = Student.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created_group.name, "ABC")
        self.assertEqual(created_student.group, created_group)

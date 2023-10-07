from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Lesson, Course, Payment
from users.models import User


class PaymentTestCase(APITestCase):

    def setUp(self) -> None:
        self.url = '/courses/payment/list/'

        self.user = User.objects.create(email='ksu@mail.ru', is_active=True, is_staff=False, is_superuser=False)
        self.manager = User.objects.create(email='manager@mail.ru', is_active=True, is_staff=False, is_superuser=False)
        group, created = Group.objects.get_or_create(name='Managers')
        self.manager.groups.add(group)

        self.some_lesson = Lesson.objects.create(
            name='test lesson',
            description='description of test lesson',
            video='https://www.youtube.com/watch?v=myf3o1CM4do&list=PLA0M1Bcd0w8yU5h2vwZ4LO7h1xt8COUXl&index=6',
            user=None
        )

        self.some_course = Course.objects.create(
            name='test anon course',
            description='description of test anon course',
            user=None
        )

        self.some_payment = Payment.objects.create(
            amount=2000,
            way_pay='cash',
            user=User.objects.create(email='some_user@mail.ru'),
            course=self.some_course,
            lesson=None
        )

        self.users_payment = Payment.objects.create(
            amount=2000,
            way_pay='card',
            user=self.user,
            course=self.some_course,
            lesson=None
        )

    def test_payment_list_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_payment_list_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['user'], self.user.pk)

    def test_payment_list_manager(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

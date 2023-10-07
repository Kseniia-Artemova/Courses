from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email='ksu@mail.ru', is_active=True, is_staff=False, is_superuser=False)
        self.course = Course.objects.create(
            name='test course',
            description='description of test course',
            user=self.user
        )
        self.url = f'/courses/subscribe/{self.course.pk}/'

    def test_subscribe_to_updates(self):

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': f'Подписан на обновления курса {self.course.name}!'})
        subscription_state = Subscription.objects.filter(course=self.course, user=self.user).exists()
        self.assertEqual(subscription_state, True)

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': f'Подписка на обновления курса {self.course.name} отменена!'})
        subscription_state = Subscription.objects.filter(course=self.course, user=self.user).exists()
        self.assertEqual(subscription_state, False)
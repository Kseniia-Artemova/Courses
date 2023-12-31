from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.url = '/courses/lessons/'

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
        self.users_lesson = Lesson.objects.create(
            name='test lesson',
            description='description of test lesson',
            video='https://www.youtube.com/watch?v=myf3o1CM4do&list=PLA0M1Bcd0w8yU5h2vwZ4LO7h1xt8COUXl&index=6',
            user=self.user
        )

        self.good_data = {
            'name': 'test usual user\'s lesson',
            'description': 'test description of usual user\'s lesson',
            'video': 'https://www.youtube.com/watch?v=EVrMbS14FdE&list=PLA0M1Bcd0w8xZA3Kl1fYmOH_MfLpiYMRs&index=2',
        }

        self.client.force_authenticate(user=self.user)

    def test_get_response_unauthorized(self):

        self.client.force_authenticate()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(self.url + f'{self.some_lesson.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(self.url, data={'name': 'test_lesson'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(self.url + f'{self.some_lesson.pk}/', data={'name': 'test_lesson_change'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(self.url + f'{self.some_lesson.pk}/', data={'name': 'test_lesson_change'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(self.url + f'{self.some_lesson.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_lesson_list(self):

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()['results'],
            [
                {
                    'name': self.some_lesson.name,
                    'description': self.some_lesson.description,
                    'video': self.some_lesson.video,
                    'user': self.some_lesson.user,
                    'course': self.some_lesson.course
                },
                {
                    'name': self.users_lesson.name,
                    'description': self.users_lesson.description,
                    'video': self.users_lesson.video,
                    'user': self.users_lesson.user.email,
                    'course': self.users_lesson.course
                }
            ]
        )

    def test_create_lesson_user(self):
        bad_data = {
            'name': 'test created lesson',
            'description': 'test description of created lesson',
            'video': 'https://www.just-test.co/',
        }

        good_data = {
            'name': 'test created lesson',
            'description': 'test description of created lesson',
            'video': 'https://www.youtube.com/watch?v=myf3o1CM4do&list=PLA0M1Bcd0w8yU5h2vwZ4LO7h1xt8COUXl&index=6',
        }

        response = self.client.post(self.url, data=bad_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.url, data=good_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.json(), {
                'name': good_data['name'],
                'description': good_data['description'],
                'video': good_data['video'],
                'user': self.user.email,
                'course': None
            }
        )

    def test_create_lesson_manager(self):
        good_data = {
            'name': 'test created lesson',
            'description': 'test description of created lesson',
            'video': 'https://www.youtube.com/watch?v=EVrMbS14FdE&list=PLA0M1Bcd0w8xZA3Kl1fYmOH_MfLpiYMRs&index=2',
        }

        self.client.force_authenticate(user=self.manager)

        response = self.client.post(self.url, data=good_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_lesson_user(self):

        response = self.client.get(self.url + f'{self.some_lesson.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(self.url + f'{self.users_lesson.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'name': self.users_lesson.name,
            'description': self.users_lesson.description,
            'video': self.users_lesson.video,
            'user': self.users_lesson.user.email,
            'course': self.users_lesson.course

        })

    def test_retrieve_lesson_manager(self):

        self.client.force_authenticate(user=self.manager)

        response = self.client.get(self.url + f'{self.users_lesson.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'name': self.users_lesson.name,
            'description': self.users_lesson.description,
            'video': self.users_lesson.video,
            'user': self.users_lesson.user.email,
            'course': self.users_lesson.course
        })

    def test_update_lesson_user(self):
        update_data = {
            'name': 'test created lesson',
            'description': 'test description of created lesson',
            'video': 'https://www.youtube.com/watch?v=EVrMbS14FdE&list=PLA0M1Bcd0w8xZA3Kl1fYmOH_MfLpiYMRs&index=2',
        }

        response = self.client.put(self.url + f'{self.some_lesson.pk}/', data=update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.patch(self.url + f'{self.some_lesson.pk}/', data={'name': 'test_update'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(self.url + f'{self.users_lesson.pk}/', data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], update_data['name'])

        response = self.client.patch(self.url + f'{self.users_lesson.pk}/', data={'name': 'test_update'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'test_update')

    def test_update_lesson_manager(self):
        update_data = {
            'name': 'test created lesson',
            'description': 'test description of created lesson',
            'video': 'https://www.youtube.com/watch?v=EVrMbS14FdE&list=PLA0M1Bcd0w8xZA3Kl1fYmOH_MfLpiYMRs&index=2',
        }

        self.client.force_authenticate(user=self.manager)

        response = self.client.put(self.url + f'{self.users_lesson.pk}/', data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], update_data['name'])

        response = self.client.patch(self.url + f'{self.users_lesson.pk}/', data={'name': 'test_update'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'test_update')

    def test_delete_lesson_user(self):

        response = self.client.delete(self.url + f'{self.some_lesson.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(self.url + f'{self.users_lesson.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_lesson_manager(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.delete(self.url + f'{self.some_lesson.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(self.url + f'{self.users_lesson.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




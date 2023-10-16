from pprint import pprint

from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from courses.models import Course
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email='ksu@mail.ru', is_active=True, is_staff=False, is_superuser=False)
        self.manager = User.objects.create(email='manager@mail.ru', is_active=True, is_staff=False, is_superuser=False)
        group, created = Group.objects.get_or_create(name='Managers')
        self.manager.groups.add(group)

        self.some_course = Course.objects.create(
            name='test anon course',
            description='description of test anon course',
            user=None
        )
        self.users_course = Course.objects.create(
            name='test user course',
            description='description of test user course',
            user=self.user
        )

        self.good_data = {
            'name': 'test usual user\'s course',
            'description': 'test description of usual user\'s course',
        }

        self.client.force_authenticate(user=self.user)

    def test_get_response_unauthorized(self):
        self.client.force_authenticate()

        response = self.client.get(reverse('courses:courses_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('courses:course_detail', args=[self.some_course.pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(reverse('courses:course_create'), data={'name': 'test_course'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(reverse('courses:course_update', args=[self.some_course.pk]),
                                   data={'name': 'test_course_change'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(reverse('courses:course_update', args=[self.some_course.pk]),
                                     data={'name': 'test_lesson_change'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(reverse('courses:course_delete', args=[self.some_course.pk]),)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_course_list(self):
        url = reverse('courses:courses_list')
        expected_response = [
            {
                'description': self.some_course.description,
                'id': self.some_course.pk,
                'is_updates_active': False,
                'lesson_count': 0,
                'lessons': [],
                'name': self.some_course.name,
                'preview': None,
                'user': self.some_course.user},
            {
                'description': self.users_course.description,
                'id': self.users_course.pk,
                'is_updates_active': False,
                'lesson_count': 0,
                'lessons': [],
                'name': self.users_course.name,
                'preview': None,
                'user': self.user.email
            }
        ]

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], expected_response)

    def test_create_course_user(self):
        url = reverse('courses:course_create')

        data = {
            'name': 'test created course',
            'description': 'test description of created course',
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.json(), {'description': data['description'],
                              'id': Course.objects.get(name=data['name']).pk,
                              'is_updates_active': False,
                              'lesson_count': 0,
                              'lessons': [],
                              'name': data['name'],
                              'preview': None,
                              'user': self.user.email}
        )

    def test_create_course_manager(self):
        url = reverse('courses:course_create')

        data = {
            'name': 'test created course',
            'description': 'test description of created course',
        }

        self.client.force_authenticate(user=self.manager)

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_course_user(self):
        url = reverse('courses:course_detail', args=[self.some_course.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('courses:course_detail', args=[self.users_course.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), {'description': self.users_course.description,
                              'id': self.users_course.pk,
                              'is_updates_active': False,
                              'lesson_count': 0,
                              'lessons': [],
                              'name': self.users_course.name,
                              'preview': None,
                              'user': self.user.email}
        )

    def test_retrieve_course_manager(self):

        self.client.force_authenticate(user=self.manager)

        url = reverse('courses:course_detail', args=[self.some_course.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), {'description': self.some_course.description,
                              'id': self.some_course.pk,
                              'is_updates_active': False,
                              'lesson_count': 0,
                              'lessons': [],
                              'name': self.some_course.name,
                              'preview': None,
                              'user': self.some_course.user}
        )

        url = reverse('courses:course_detail', args=[self.users_course.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), {'description': self.users_course.description,
                              'id': self.users_course.pk,
                              'is_updates_active': False,
                              'lesson_count': 0,
                              'lessons': [],
                              'name': self.users_course.name,
                              'preview': None,
                              'user': self.user.email}
        )

    def test_update_course_user(self):
        update_data = {
            'name': 'test created course',
            'description': 'test description of created course'
        }

        url = reverse('courses:course_update', args=[self.some_course.pk])

        response = self.client.put(url, data=update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.patch(url, data={'name': 'test_update'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('courses:course_update', args=[self.users_course.pk])

        response = self.client.put(url, data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], update_data['name'])

        response = self.client.patch(url, data={'name': 'test_update'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'test_update')

    def test_update_course_manager(self):
        update_data = {
            'name': 'test created course',
            'description': 'test description of created course'
        }

        self.client.force_authenticate(user=self.manager)

        url = reverse('courses:course_update', args=[self.some_course.pk])

        response = self.client.put(url, data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], update_data['name'])

        response = self.client.patch(url, data={'name': 'test_update'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'test_update')

        url = reverse('courses:course_update', args=[self.users_course.pk])

        response = self.client.put(url, data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], update_data['name'])

        response = self.client.patch(url, data={'name': 'test_update'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'test_update')

    def test_delete_lesson_user(self):

        url = reverse('courses:course_delete', args=[self.some_course.pk])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('courses:course_delete', args=[self.users_course.pk])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_lesson_manager(self):
        self.client.force_authenticate(user=self.manager)

        url = reverse('courses:course_delete', args=[self.some_course.pk])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('courses:course_delete', args=[self.users_course.pk])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

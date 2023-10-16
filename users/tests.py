from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):

    def setUp(self) -> None:
        self.url = '/users/'

        self.user = User.objects.create(email='ksu@mail.ru', is_active=True, is_staff=False, is_superuser=False)
        self.other_user = User.objects.create(email='other_user@mail.ru')

        self.client.force_authenticate(user=self.user)

    def test_create_user(self):

        response = self.client.post(self.url, data={'email': 'created_user@mail.ru', 'password': 'zmeyalucifer1010'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(),
                         {
                             'email': 'created_user@mail.ru',
                             'phone': None,
                             'city': None,
                             'avatar': None,
                             'payments': []
                         }
                         )
        response = self.client.post(self.url, data={'email': 'created_user@mail.ru', 'password': 'zmeyalucifer1010'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.force_authenticate()

        response = self.client.post(self.url, data={'email': 'new_user@mail.ru', 'password': 'zmeyalucifer1010'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(),
                         {
                             'email': 'new_user@mail.ru',
                             'phone': None,
                             'city': None,
                             'avatar': None,
                             'payments': []
                         }
                         )

    def test_list_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

        self.client.force_authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user(self):
        response = self.client.get(self.url + f'{self.user.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'email': self.user.email,
            'phone': self.user.phone,
            'city': self.user.city,
            'avatar': self.user.avatar
            }
        )

        response = self.client.get(self.url + f'{self.other_user.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'email': self.other_user.email,
            'phone': self.other_user.phone,
            'city': self.other_user.city,
            'avatar': self.other_user.avatar
            }
        )

        self.client.force_authenticate()
        response = self.client.get(self.url + f'{self.user.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user(self):
        response = self.client.put(self.url + f'{self.user.pk}/', data={
            'email': 'update_user_1@mail.ru',
            'password': 'zmeyalucifer1010'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'avatar': None,
            'city': None,
            'email': 'update_user_1@mail.ru',
            'payments': [],
            'phone': None
            }
        )

        response = self.client.put(self.url + f'{self.other_user.pk}/', data={
            'email': 'update_user_2@mail.ru',
            'password': 'zmeyalucifer1010'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.user.refresh_from_db()

        response = self.client.patch(self.url + f'{self.user.pk}/', data={'email': 'update_user_3@mail.ru'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'avatar': None,
            'city': None,
            'email': 'update_user_3@mail.ru',
            'payments': [],
            'phone': None
            }
        )

        response = self.client.patch(self.url + f'{self.other_user.pk}/', data={'email': 'update_user_4@mail.ru'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate()

        response = self.client.put(self.url + f'{self.user.pk}/', data={
            'email': 'update_user_2@mail.ru',
            'password': 'zmeyalucifer1010'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(self.url + f'{self.user.pk}/', data={'email': 'update_user_4@mail.ru'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user(self):
        response = self.client.delete(self.url + f'{self.other_user.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(self.url + f'{self.user.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_unauthenticated(self):
        self.client.force_authenticate()
        response = self.client.delete(self.url + f'{self.other_user.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(self.url + f'{self.user.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

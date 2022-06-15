import uuid
from django.test import TestCase
from django_hosts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.User.models import User
from core.User.factories import UserFactory
from core.Profile.models import Profile
from core.Profile.factories import ProfileFactory


class ApiUserViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory.create()
        self.profile = ProfileFactory.create(user=self.user)

        self.superuser = UserFactory.create(is_active=True, is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.superuser)

        self.users_data = {
            "email": "user@example.com",
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
            "first_name": "First name",
            "last_name": "Last name",
            "middle_name": "Middle name"
        }

        self.passwd = str(uuid.uuid4()).replace('-', '')[:32]

    def test_users_list(self):
        response = self.client.get(reverse('api-v1:users-list', host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        self.assertEqual(len(results), 2)
        self.assertContains(response, self.user.id)
        self.assertContains(response, self.superuser.id)

    def test_users_create_success(self):
        data = self.users_data.copy()
        response = self.client.post(reverse('api-v1:users-list', host='api'),
                                    HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        result = response.data
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_users_update_success(self):
        data = self.users_data.copy()
        response = self.client.put(reverse('api-v1:users-detail', args=[self.user.id], host='api'),
                                   HTTP_HOST='api', format='json', data=data)
        result = response.data
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_users_retrieve_success(self):
        response = self.client.get(reverse('api-v1:users-detail', args=[self.user.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user.id)

    def test_users_delete_success(self):
        response = self.client.delete(reverse('api-v1:users-detail', args=[self.user.id], host='api'),
                                      HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertFalse(Profile.objects.all().exists())

    def test_users_archive(self):
        response = self.client.post(reverse('api-v1:users-archive', args=[self.user.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user.id)

    def test_users_restore(self):
        response = self.client.post(reverse('api-v1:users-restore', args=[self.user.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user.id)

    def test_users_set_password_not_complex_success(self):
        passwd = self.passwd
        data = {
            'disable_complex_password': True,
            'password': passwd,
            'repeat_password': passwd,
        }
        response = self.client.post(reverse('api-v1:users-set-password', args=[self.user.id], host='api'),
                                    HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_set_password_complex_success(self):
        symbols = ['@', '$', '&', '.']
        passwd = self.passwd
        for symbol in symbols:
            current_psw = passwd[:24] + 'Q' + symbol
            data = {
                'password': current_psw,
                'repeat_password': current_psw,
            }
            response = self.client.post(reverse('api-v1:users-set-password', args=[self.user.id], host='api'),
                                        HTTP_HOST='api', format='json', data=data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_set_password_mismatch_exception(self):
        data = {
            'disable_complex_password': True,
            'password': str(uuid.uuid4())[:30],
            'repeat_password': str(uuid.uuid4())[:30],
        }
        response = self.client.post(reverse('api-v1:users-set-password', args=[self.user.id], host='api'),
                                    HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_users_user_get_profiles_success(self):
        response = self.client.get(reverse('api-v1:users-profiles', args=[self.user.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.profile.id)

    def test_users_user_forbidden(self):
        user = UserFactory.create(is_active=True, is_staff=False, is_superuser=False)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('api-v1:users-list', host='api'),
                              HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_staff_forbidden(self):
        user = UserFactory.create(is_active=True, is_staff=True, is_superuser=False)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('api-v1:users-list', host='api'),
                              HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

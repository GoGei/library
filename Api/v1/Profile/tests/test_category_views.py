from django.test import TestCase
from django_hosts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.User.factories import UserFactory
from core.Profile.models import Profile
from core.Profile.factories import ProfileFactory


class ApiProfileViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory.create()
        self.profile = ProfileFactory.create(user=self.user)

        self.superuser = UserFactory.create(is_active=True, is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.superuser)

        user = UserFactory.create()
        self.profile_data = {
            'user': user.id,
        }
        self.user_data = {

        }

    def test_profile_list(self):
        response = self.client.get(reverse('api-v1:profile-list', host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.profile.id)

    def test_profile_create_success(self):
        data = self.profile_data.copy()
        response = self.client.post(reverse('api-v1:profile-list', host='api'),
                                    HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        result = response.data
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_profile_update_success(self):
        data = self.profile_data.copy()
        response = self.client.put(reverse('api-v1:profile-detail', args=[self.profile.id], host='api'),
                                   HTTP_HOST='api', format='json', data=data)
        result = response.data
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_profile_retrieve_success(self):
        response = self.client.get(reverse('api-v1:profile-detail', args=[self.profile.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.profile.id)

    def test_profile_delete_success(self):
        response = self.client.delete(reverse('api-v1:profile-detail', args=[self.profile.id], host='api'),
                                      HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Profile.objects.all().exists())

    def test_profile_archive(self):
        profile = self.profile
        user = self.profile.user

        response = self.client.post(reverse('api-v1:profile-archive', args=[profile.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, profile.id)
        self.assertContains(response, user.id)

    def test_profile_restore(self):
        profile = self.profile
        user = self.profile.user

        response = self.client.post(reverse('api-v1:profile-restore', args=[profile.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, profile.id)
        self.assertContains(response, user.id)

    def test_profile_user_forbidden(self):
        user = UserFactory.create(is_active=True, is_staff=False, is_superuser=False)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(reverse('api-v1:profile-list', host='api'),
                               HTTP_HOST='api', format='json', data=self.profile_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_staff_forbidden(self):
        user = UserFactory.create(is_active=True, is_staff=True, is_superuser=False)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(reverse('api-v1:profile-list', host='api'),
                               HTTP_HOST='api', format='json', data=self.profile_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

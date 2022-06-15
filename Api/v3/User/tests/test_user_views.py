from django.test import TestCase
from django_hosts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.User.factories import UserFactory
from core.Profile.factories import ProfileFactory


class ApiUserViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory.create()
        self.profile = ProfileFactory.create(user=self.user)

        self.superuser = UserFactory.create(is_active=True, is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.superuser)

    def test_users_list(self):
        response = self.client.get(reverse('api-v3:users-list', host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        self.assertEqual(len(results), 2)
        self.assertContains(response, self.user.id)
        self.assertContains(response, self.superuser.id)

    def test_users_retrieve_success(self):
        response = self.client.get(reverse('api-v3:users-detail', args=[self.user.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user.id)

    def test_users_user_get_profiles_success(self):
        response = self.client.get(reverse('api-v3:users-profiles', args=[self.user.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.profile.id)

    def test_users_user_forbidden(self):
        user = UserFactory.create(is_active=True, is_staff=False, is_superuser=False)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('api-v3:users-list', host='api'),
                              HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

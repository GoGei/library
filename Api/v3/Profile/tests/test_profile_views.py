from django.test import TestCase
from django_hosts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.User.factories import UserFactory
from core.Profile.factories import ProfileFactory


class ApiProfileViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory.create()
        self.profile = ProfileFactory.create(user=self.user)

        self.staff = UserFactory.create(is_active=True, is_staff=True, is_superuser=False)
        self.client.force_authenticate(user=self.staff)

        user = UserFactory.create()
        self.profile_data = {
            'user': user.id,
        }

    def test_profile_list(self):
        response = self.client.get(reverse('api-v3:profiles-list', host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.profile.id)

    def test_profile_retrieve_success(self):
        response = self.client.get(reverse('api-v3:profiles-detail', args=[self.profile.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.profile.id)

    def test_profile_user_forbidden(self):
        user = UserFactory.create(is_active=True, is_staff=False, is_superuser=False)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('api-v3:profiles-list', host='api'),
                              HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

from django.test import TestCase
from django_hosts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.User.factories import UserFactory
from core.Book.factories import BookFactory
from core.Favourite.models import Favourite
from core.Favourite.factories import FavouriteFactory


class ApiFavouriteViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = BookFactory.create()

        self.superuser = UserFactory.create(is_active=True, is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.superuser)

        self.favourite = FavouriteFactory.create(user=self.superuser, book=self.book)

        user = UserFactory.create()
        book = BookFactory.create()
        self.favourite_data = {
            'user': user.id,
            'book': book.id,
            'is_favourite': True,
        }
        self.favourite_new_data = self.favourite_data.copy()
        self.favourite_new_data.update({
            'is_favourite': False,
        })

    def test_favourite_list(self):
        response = self.client.get(reverse('api-v1:favourite-list', host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.favourite.id)

    def test_favourite_create_success(self):
        data = self.favourite_data.copy()
        response = self.client.post(reverse('api-v1:favourite-list', host='api'),
                                    HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        result = response.data
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_favourite_update_success(self):
        data = self.favourite_new_data.copy()
        response = self.client.put(reverse('api-v1:favourite-detail', args=[self.favourite.id], host='api'),
                                   HTTP_HOST='api', format='json', data=data)
        result = response.data
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_favourite_retrieve_success(self):
        response = self.client.get(reverse('api-v1:favourite-detail', args=[self.favourite.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.favourite.id)

    def test_favourite_delete_success(self):
        response = self.client.delete(reverse('api-v1:favourite-detail', args=[self.favourite.id], host='api'),
                                      HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Favourite.objects.all().exists())

    def test_favourite_user_forbidden(self):
        user = UserFactory.create(is_active=True, is_staff=False, is_superuser=False)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(reverse('api-v1:favourite-list', host='api'),
                               HTTP_HOST='api', format='json', data=self.favourite_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_favourite_staff_forbidden(self):
        user = UserFactory.create(is_active=True, is_staff=True, is_superuser=False)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(reverse('api-v1:favourite-list', host='api'),
                               HTTP_HOST='api', format='json', data=self.favourite_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

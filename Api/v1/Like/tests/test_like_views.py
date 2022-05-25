from django.test import TestCase
from django_hosts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.User.factories import UserFactory
from core.Book.factories import BookFactory
from core.Like.models import Like
from core.Like.factories import LikeFactory


class ApiLikeViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = BookFactory.create()

        self.superuser = UserFactory.create(is_active=True, is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.superuser)

        self.like = LikeFactory.create(user=self.superuser, book=self.book)

        user = UserFactory.create()
        book = BookFactory.create()
        self.like_data = {
            'user': user.id,
            'book': book.id,
            'is_liked': True,
        }
        self.like_new_data = self.like_data.copy()
        self.like_new_data.update({
            'is_liked': False,
        })

    def test_like_list(self):
        response = self.client.get(reverse('api-v1:like-list', host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.like.id)

    def test_like_create_success(self):
        data = self.like_data.copy()
        response = self.client.post(reverse('api-v1:like-list', host='api'),
                                    HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        result = response.data
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_like_update_success(self):
        data = self.like_new_data.copy()
        response = self.client.put(reverse('api-v1:like-detail', args=[self.like.id], host='api'),
                                   HTTP_HOST='api', format='json', data=data)
        result = response.data
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_like_retrieve_success(self):
        response = self.client.get(reverse('api-v1:like-detail', args=[self.like.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.like.id)

    def test_like_delete_success(self):
        response = self.client.delete(reverse('api-v1:like-detail', args=[self.like.id], host='api'),
                                      HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Like.objects.all().exists())

    def test_like_user_forbidden(self):
        user = UserFactory.create(is_active=True, is_staff=False, is_superuser=False)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(reverse('api-v1:like-list', host='api'),
                               HTTP_HOST='api', format='json', data=self.like_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_like_staff_forbidden(self):
        user = UserFactory.create(is_active=True, is_staff=True, is_superuser=False)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(reverse('api-v1:like-list', host='api'),
                               HTTP_HOST='api', format='json', data=self.like_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

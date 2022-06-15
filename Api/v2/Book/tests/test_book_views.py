from django.test import TestCase
from django_hosts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.Book.factories import BookFactory
from core.User.factories import UserFactory


class ApiBookViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = BookFactory.create()

        self.user = UserFactory.create()
        self.client.force_authenticate(user=self.user)

    def test_book_list(self):
        response = self.client.get(reverse('api-v2:books-list', host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.book.id)

    def test_book_retrieve_success(self):
        response = self.client.get(reverse('api-v2:books-detail', args=[self.book.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.book.id)

    def test_book_like(self):
        book = self.book
        response = self.client.post(reverse('api-v2:books-like', args=[book.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, book.id)
        self.assertTrue(book.like_set.all().first().is_liked)

    def test_book_dislike(self):
        book = self.book
        response = self.client.post(reverse('api-v2:books-dislike', args=[book.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, book.id)
        self.assertFalse(book.like_set.all().first().is_liked)

    def test_book_deactivate(self):
        book = self.book
        response = self.client.post(reverse('api-v2:books-deactivate', args=[book.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, book.id)
        self.assertIsNone(book.like_set.all().first().is_liked)

    def test_book_favour(self):
        book = self.book
        response = self.client.post(reverse('api-v2:books-favour', args=[book.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, book.id)
        self.assertTrue(book.favourite_set.all().first().is_favourite)

    def test_book_unfavour(self):
        book = self.book
        response = self.client.post(reverse('api-v2:books-unfavour', args=[book.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, book.id)
        self.assertFalse(book.favourite_set.all().first().is_favourite)

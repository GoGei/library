from django.utils import timezone
from django.test import TestCase
from django_hosts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.User.factories import UserFactory
from core.Book.models import Book
from core.Book.factories import BookFactory
from core.Category.factories import CategoryFactory
from core.Author.factories import AuthorFactory


class ApiBookViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = BookFactory.create()

        self.superuser = UserFactory.create(is_active=True, is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.superuser)

        category = CategoryFactory.create()
        author = AuthorFactory.create()
        self.book_data = {
            'name': 'book-name',
            'category': [category.id],
            'author': author.id,
            'publish_date': timezone.now().date().strftime('%Y-%m-%d'),
            'description': 'description',
        }
        self.book_new_data = self.book_data.copy()
        self.book_new_data.update({
            'name': 'book-new-name',
        })

    def test_book_list(self):
        response = self.client.get(reverse('api-v1:books-list', host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.book.id)

    def test_book_create_success(self):
        data = self.book_data.copy()
        response = self.client.post(reverse('api-v1:books-list', host='api'),
                                    HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        result = response.data
        self.assertTrue(Book.objects.filter(slug=result['slug']))
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_book_create_name_error(self):
        data = self.book_data.copy()
        self.client.post(reverse('api-v1:books-list', host='api'),
                         HTTP_HOST='api', format='json', data=data)
        response = self.client.post(reverse('api-v1:books-list', host='api'),
                                    HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        result = response.data
        self.assertIn('name', result)

    def test_book_update_success(self):
        data = self.book_new_data.copy()
        response = self.client.put(reverse('api-v1:books-detail', args=[self.book.id], host='api'),
                                   HTTP_HOST='api', format='json', data=data)
        result = response.data
        self.assertTrue(Book.objects.filter(slug=result['slug']))
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_book_update_name_error(self):
        data = self.book_data.copy()
        self.client.post(reverse('api-v1:books-list', host='api'), HTTP_HOST='api', format='json', data=data)
        response = self.client.put(reverse('api-v1:books-detail', args=[self.book.id], host='api'),
                                   HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = response.data
        self.assertIn('name', result)

    def test_book_retrieve_success(self):
        response = self.client.get(reverse('api-v1:books-detail', args=[self.book.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.book.id)

    def test_book_delete_success(self):
        response = self.client.delete(reverse('api-v1:books-detail', args=[self.book.id], host='api'),
                                      HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.all().exists())

    def test_book_archive(self):
        book = self.book

        response = self.client.post(reverse('api-v1:books-archive', args=[book.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, book.id)

    def test_book_restore(self):
        book = self.book

        response = self.client.post(reverse('api-v1:books-restore', args=[book.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, book.id)

    def test_book_like(self):
        book = self.book

        response = self.client.post(reverse('api-v1:books-like', args=[book.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, book.id)
        self.assertTrue(book.like_set.all().first().is_liked)

    def test_book_dislike(self):
        book = self.book

        response = self.client.post(reverse('api-v1:books-dislike', args=[book.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, book.id)
        self.assertFalse(book.like_set.all().first().is_liked)

    def test_book_deactivate(self):
        book = self.book

        response = self.client.post(reverse('api-v1:books-deactivate', args=[book.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, book.id)
        self.assertIsNone(book.like_set.all().first().is_liked)

    def test_book_favour(self):
        book = self.book

        response = self.client.post(reverse('api-v1:books-favour', args=[book.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, book.id)
        self.assertTrue(book.favourite_set.all().first().is_favourite)

    def test_book_unfavour(self):
        book = self.book

        response = self.client.post(reverse('api-v1:books-unfavour', args=[book.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, book.id)
        self.assertFalse(book.favourite_set.all().first().is_favourite)

    def test_book_user_forbidden(self):
        user = UserFactory.create(is_active=True, is_staff=False, is_superuser=False)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('api-v1:books-list', host='api'),
                              HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_staff_forbidden(self):
        user = UserFactory.create(is_active=True, is_staff=True, is_superuser=False)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('api-v1:books-list', host='api'),
                              HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

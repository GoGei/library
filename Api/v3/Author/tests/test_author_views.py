from django.test import TestCase
from django_hosts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.User.factories import UserFactory
from core.Author.models import Author
from core.Author.factories import AuthorFactory
from core.Book.factories import BookFactory


class ApiAuthorViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = AuthorFactory.create()
        self.book = BookFactory.create(author=self.author)

        self.staff = UserFactory.create(is_active=True, is_staff=True, is_superuser=False)
        self.client.force_authenticate(user=self.staff)

        self.author_data = {
            'first_name': 'author first name',
            'last_name': 'author last name',
            'middle_name': 'author middle name',
        }
        self.author_new_data = {
            'first_name': 'author first name new',
            'last_name': 'author last name new',
            'middle_name': 'author middle name new',
        }

    def test_author_list(self):
        response = self.client.get(reverse('api-v3:authors-list', host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.author.id)

    def test_author_create_success(self):
        data = self.author_data.copy()
        response = self.client.post(reverse('api-v3:authors-list', host='api'),
                                    HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        result = response.data
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_author_update_success(self):
        data = self.author_new_data.copy()
        response = self.client.put(reverse('api-v3:authors-detail', args=[self.author.id], host='api'),
                                   HTTP_HOST='api', format='json', data=data)
        result = response.data
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_author_retrieve_success(self):
        response = self.client.get(reverse('api-v3:authors-detail', args=[self.author.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.author.id)

    def test_author_delete_success(self):
        self.book.delete()
        response = self.client.delete(reverse('api-v3:authors-detail', args=[self.author.id], host='api'),
                                      HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
        self.assertFalse(Author.objects.all().exists())

    def test_author_delete_model_protect_success(self):
        response = self.client.delete(reverse('api-v3:authors-detail', args=[self.author.id], host='api'),
                                      HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_author_archive(self):
        response = self.client.post(reverse('api-v3:authors-archive', args=[self.author.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_author_restore(self):
        response = self.client.post(reverse('api-v3:authors-restore', args=[self.author.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_author_user_forbidden(self):
        user = UserFactory.create(is_active=True, is_staff=False, is_superuser=False)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('api-v3:authors-list', host='api'),
                              HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

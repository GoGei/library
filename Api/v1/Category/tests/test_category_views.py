from django.test import TestCase
from django_hosts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.User.factories import UserFactory
from core.Category.models import Category
from core.Category.factories import CategoryFactory
from core.Book.factories import BookFactory


class ApiCategoryViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = CategoryFactory.create()
        self.book = BookFactory.create(category=[self.category])

        self.superuser = UserFactory.create(is_active=True, is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.superuser)

        self.category_data = {
            'name': 'category-name',
        }
        self.category_new_data = {
            'name': 'category-new-name',
        }

    def test_category_list(self):
        response = self.client.get(reverse('api-v1:categories-list', host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.category.id)

    def test_category_create_success(self):
        data = self.category_data.copy()
        response = self.client.post(reverse('api-v1:categories-list', host='api'),
                                    HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        result = response.data
        self.assertTrue(Category.objects.filter(slug=result['slug']))
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_category_create_name_error(self):
        data = self.category_data.copy()
        self.client.post(reverse('api-v1:categories-list', host='api'),
                         HTTP_HOST='api', format='json', data=data)
        response = self.client.post(reverse('api-v1:categories-list', host='api'),
                                    HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        result = response.data
        self.assertIn('name', result)

    def test_category_update_success(self):
        data = self.category_new_data.copy()
        response = self.client.put(reverse('api-v1:categories-detail', args=[self.category.id], host='api'),
                                   HTTP_HOST='api', format='json', data=data)
        result = response.data
        self.assertTrue(Category.objects.filter(slug=result['slug']))
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_category_update_name_error(self):
        data = self.category_data.copy()
        self.client.post(reverse('api-v1:categories-list', host='api'), HTTP_HOST='api', format='json', data=data)
        response = self.client.put(reverse('api-v1:categories-detail', args=[self.category.id], host='api'),
                                   HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = response.data
        self.assertIn('name', result)

    def test_category_retrieve_success(self):
        response = self.client.get(reverse('api-v1:categories-detail', args=[self.category.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.category.id)

    def test_category_delete_success(self):
        response = self.client.delete(reverse('api-v1:categories-detail', args=[self.category.id], host='api'),
                                      HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.all().exists())

    def test_category_archive(self):
        category = self.category
        book = self.book

        response = self.client.post(reverse('api-v1:categories-archive', args=[category.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, category.id)
        self.assertContains(response, book.id)

    def test_category_restore(self):
        category = self.category
        book = self.book

        response = self.client.post(reverse('api-v1:categories-restore', args=[category.id], host='api'),
                                    HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, category.id)
        self.assertContains(response, book.id)

    def test_category_user_forbidden(self):
        user = UserFactory.create(is_active=True, is_staff=False, is_superuser=False)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(reverse('api-v1:categories-list', host='api'),
                               HTTP_HOST='api', format='json', data=self.category_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_staff_forbidden(self):
        user = UserFactory.create(is_active=True, is_staff=True, is_superuser=False)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(reverse('api-v1:categories-list', host='api'),
                               HTTP_HOST='api', format='json', data=self.category_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

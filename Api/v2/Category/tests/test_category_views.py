from django.test import TestCase
from django_hosts import reverse
from rest_framework import status

from core.Category.factories import CategoryFactory


class ApiCategoryViewTests(TestCase):
    def setUp(self):
        self.category = CategoryFactory.create()

    def test_category_list(self):
        response = self.client.get(reverse('api-v2:categories-list', host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.category.id)

    def test_category_retrieve_success(self):
        response = self.client.get(reverse('api-v2:categories-detail', args=[self.category.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.category.id)

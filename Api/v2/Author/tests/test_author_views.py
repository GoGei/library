from django.test import TestCase
from django_hosts import reverse
from rest_framework import status

from core.Author.factories import AuthorFactory


class ApiAuthorViewTests(TestCase):
    def setUp(self):
        self.author = AuthorFactory.create()

    def test_author_list(self):
        response = self.client.get(reverse('api-v2:authors-list', host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.author.id)

    def test_author_retrieve_success(self):
        response = self.client.get(reverse('api-v2:authors-detail', args=[self.author.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.author.id)

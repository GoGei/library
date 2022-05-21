from django.test import TestCase

from ..models import Author
from ..factories import AuthorFactory


class AuthorTests(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        obj = AuthorFactory.create()
        qs = Author.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = AuthorFactory.create()
        obj.delete()

        qs = Author.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

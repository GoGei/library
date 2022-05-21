from django.test import TestCase

from ..models import Book
from ..factories import BookFactory


class BookTests(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        obj = BookFactory.create()
        qs = Book.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = BookFactory.create()
        obj.delete()

        qs = Book.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

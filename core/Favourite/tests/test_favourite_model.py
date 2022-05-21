from django.test import TestCase

from ..models import Favourite
from ..factories import FavouriteFactory
from core.User.factories import UserFactory
from core.Book.factories import BookFactory


class FavouriteTests(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        obj = FavouriteFactory.create()
        qs = Favourite.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = FavouriteFactory.create()
        obj.delete()

        qs = Favourite.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_delete_cascade_user(self):
        user = UserFactory.create()
        obj = FavouriteFactory.create(user=user)
        user.delete()

        qs = Favourite.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_delete_cascade_post(self):
        book = BookFactory.create()
        obj = FavouriteFactory.create(book=book)
        book.delete()

        qs = Favourite.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

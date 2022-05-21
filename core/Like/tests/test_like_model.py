from django.test import TestCase

from ..models import Like
from ..factories import LikeFactory
from core.User.factories import UserFactory
from core.Book.factories import BookFactory


class LikeTests(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        obj = LikeFactory.create()
        qs = Like.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = LikeFactory.create()
        obj.delete()

        qs = Like.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_delete_cascade_user(self):
        user = UserFactory.create()
        obj = LikeFactory.create(user=user)
        user.delete()

        qs = Like.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_delete_cascade_post(self):
        book = BookFactory.create()
        obj = LikeFactory.create(book=book)
        book.delete()

        qs = Like.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

from django.test import TestCase

from ..models import Profile
from ..factories import ProfileFactory


class ProfileTests(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        obj = ProfileFactory.create()
        qs = Profile.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = ProfileFactory.create()
        obj.delete()

        qs = Profile.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

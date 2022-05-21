import factory
from factory import SubFactory
from core.User.factories import UserFactory
from .models import Profile


class ProfileFactory(factory.DjangoModelFactory):
    user = SubFactory(UserFactory)

    class Meta:
        model = Profile

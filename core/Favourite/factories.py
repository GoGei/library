import factory
from factory import SubFactory
from core.User.factories import UserFactory
from core.Book.factories import BookFactory
from .models import Favourite


class FavouriteFactory(factory.DjangoModelFactory):
    is_favourite = True
    user = SubFactory(UserFactory)
    book = SubFactory(BookFactory)

    class Meta:
        model = Favourite

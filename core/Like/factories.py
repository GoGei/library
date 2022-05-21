import factory
from factory import SubFactory
from core.User.factories import UserFactory
from core.Book.factories import BookFactory
from .models import Like


class LikeFactory(factory.DjangoModelFactory):
    is_liked = True
    user = SubFactory(UserFactory)
    book = SubFactory(BookFactory)

    class Meta:
        model = Like

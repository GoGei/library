import factory
from factory import fuzzy, SubFactory
from django.utils import timezone

from core.Author.factories import AuthorFactory
from .models import Book


class BookFactory(factory.DjangoModelFactory):
    name = fuzzy.FuzzyText(length=50)
    author = SubFactory(AuthorFactory)
    publish_date = fuzzy.FuzzyDate(start_date=timezone.now().date())

    class Meta:
        model = Book

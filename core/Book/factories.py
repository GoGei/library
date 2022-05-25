import factory
from factory import fuzzy, SubFactory
from django.utils import timezone

from core.Author.factories import AuthorFactory
from .models import Book


class BookFactory(factory.DjangoModelFactory):
    name = fuzzy.FuzzyText(length=50)
    description = fuzzy.FuzzyText(length=1000)
    author = SubFactory(AuthorFactory)
    publish_date = fuzzy.FuzzyDate(start_date=timezone.now().date())

    class Meta:
        model = Book

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            for category in extracted:
                self.category.add(category)

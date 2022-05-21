import factory
from factory import fuzzy
from .models import Author


class AuthorFactory(factory.DjangoModelFactory):
    first_name = fuzzy.FuzzyText(length=50)
    last_name = fuzzy.FuzzyText(length=50)
    middle_name = fuzzy.FuzzyText(length=50)

    class Meta:
        model = Author

import factory
from factory import fuzzy
from django.utils.text import slugify
from .models import Category


class CategoryFactory(factory.DjangoModelFactory):
    name = fuzzy.FuzzyText(length=50)
    slug = factory.LazyAttribute(lambda o: slugify(o.name))

    class Meta:
        model = Category

from django.db import models
from core.Utils.Mixins.models import CrmMixin


class Book(CrmMixin):
    name = models.CharField(max_length=255)
    category = models.ManyToManyField('Category.Category')
    author = models.ForeignKey('Author.Author', on_delete=models.PROTECT)
    publish_date = models.DateField()

    class Meta:
        db_table = 'book'

    def __str__(self):
        return self.label

    @property
    def label(self):
        return self.name

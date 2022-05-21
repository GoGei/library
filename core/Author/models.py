from django.db import models
from core.Utils.Mixins.models import CrmMixin


class Author(CrmMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'author'

    def __str__(self):
        return self.label

    @property
    def label(self):
        elems = [elem for elem in [self.first_name, self.last_name, self.middle_name] if elem]
        return ', '.join(elems)

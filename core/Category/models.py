from django.db import models
from core.Utils.Mixins.models import CrmMixin, SlugifyMixin


class Category(CrmMixin, SlugifyMixin):
    SLUGIFY_FIELD = 'name'
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.label

    @property
    def label(self):
        return self.name or str(self.id)

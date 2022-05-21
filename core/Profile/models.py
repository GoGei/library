from django.db import models
from core.Utils.Mixins.models import CrmMixin


class Profile(CrmMixin):
    user = models.ForeignKey('User.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.label

    @property
    def label(self):
        return 'Profile: %s' % self.user.label

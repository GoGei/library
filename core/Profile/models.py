from django.db import models
from core.Utils.Mixins.models import CrmMixin, ActiveQuerySet


class ProfileQuerySet(ActiveQuerySet):
    def banned(self):
        return self.filter(is_banned=False).all()

    def active(self):
        return super(ProfileQuerySet, self).active().filter(is_banned=True).all()


class Profile(CrmMixin):
    user = models.ForeignKey('User.User', on_delete=models.CASCADE)
    is_banned = models.BooleanField(default=False)

    objects = ProfileQuerySet.as_manager()

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.label

    @property
    def label(self):
        return 'Profile: %s' % self.user.label

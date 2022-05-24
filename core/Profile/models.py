from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

from core.Utils.Mixins.models import CrmMixin, ActiveQuerySet


class ProfileQuerySet(ActiveQuerySet):
    def banned(self):
        return self.filter(is_banned=False).all()

    def active(self):
        return super(ProfileQuerySet, self).active().filter(is_banned=True).all()


def default_expire_date():
    now = timezone.now()
    return (now + timezone.timedelta(days=90)).date()


class Profile(CrmMixin):
    user = models.ForeignKey('User.User', on_delete=models.CASCADE)
    is_banned = models.BooleanField(default=False)
    expire_date = models.DateField(null=True, default=default_expire_date)

    objects = ProfileQuerySet.as_manager()

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.label

    @property
    def label(self):
        return 'Profile: %s' % self.user.label

    @cached_property
    def is_expired(self):
        expired = self.expire_date
        now = timezone.now().date()
        if not expired:
            # infinitive profile
            return False
        return now > expired

    def extend_expire(self, days):
        self.expire_date += timezone.timedelta(days=days)
        self.save()

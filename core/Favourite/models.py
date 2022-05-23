from django.db import models


class FavouriteQuerySet(models.QuerySet):
    def favourites(self, user):
        return self.select_related('user', 'book').filter(user=user).all()


class Favourite(models.Model):
    is_favourite = models.BooleanField(default=False)
    user = models.ForeignKey('User.User', on_delete=models.CASCADE)
    book = models.ForeignKey('Book.Book', on_delete=models.CASCADE)

    objects = FavouriteQuerySet.as_manager()

    class Meta:
        db_table = 'favourite'

    def favourite(self):
        self.is_favourite = True
        self.save()

    def deactivate(self):
        self.is_favourite = False
        self.save()

from django.db import models


class Favourite(models.Model):
    is_favourite = models.BooleanField(default=False)
    user = models.ForeignKey('User.User', on_delete=models.CASCADE)
    book = models.ForeignKey('Book.Book', on_delete=models.CASCADE)

    class Meta:
        db_table = 'favourite'

    def favourite(self):
        self.is_favourite = True
        self.save()

    def deactivate(self):
        self.is_favourite = False
        self.save()

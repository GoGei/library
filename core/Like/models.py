from django.db import models


class Like(models.Model):
    is_liked = models.BooleanField(null=True, default=None)
    user = models.ForeignKey('User.User', on_delete=models.CASCADE)
    book = models.ForeignKey('Book.Book', on_delete=models.CASCADE)

    class Meta:
        db_table = 'like'

    def like(self):
        self.is_liked = True
        self.save()

    def dislike(self):
        self.is_liked = False
        self.save()

    def deactivate(self):
        self.is_liked = None
        self.save()

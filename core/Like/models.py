from django.db import models


class LikeQuerySet(models.QuerySet):
    def liked(self, user):
        return self.select_related('user', 'book').filter(user=user, is_liked=True).all()

    def disliked(self, user):
        return self.select_related('user', 'book').filter(user=user, is_liked=False).all()


class Like(models.Model):
    is_liked = models.BooleanField(null=True, default=None)
    user = models.ForeignKey('User.User', on_delete=models.CASCADE)
    book = models.ForeignKey('Book.Book', on_delete=models.CASCADE)

    objects = LikeQuerySet.as_manager()

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

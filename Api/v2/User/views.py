from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer
from core.User.models import User
from core.Book.models import Book


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        book_qs = Book.objects.select_related('author').prefetch_related('category').active()
        user = get_object_or_404(User.objects.prefetch_related('profile_set', 'like_set', 'favourite_set'),
                                 pk=request.user.pk)

        liked = user.like_set.all().values_list('book', flat=True).distinct()
        liked = book_qs.filter(id__in=liked)
        favourite = user.favourite_set.all().values_list('book', flat=True).distinct()
        favourite = book_qs.filter(id__in=favourite)
        profile = user.profile_set.all().ordered().first()

        setattr(user, 'liked', liked)
        setattr(user, 'favourite', favourite)
        setattr(user, 'profile', profile)

        serializer = ProfileSerializer(user)
        return Response(serializer.data)

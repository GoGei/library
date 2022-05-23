from django.db.models.expressions import RawSQL
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from core.Book.models import Book
from core.Like.models import Like
from core.Favourite.models import Favourite

from .serializers import BookSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Book.objects.select_related('author').prefetch_related('category').active()
    serializer_class = BookSerializer

    filterset_fields = ['author', 'category']
    ordering_fields = ['name', 'publish_date']
    search_fields = ['name', 'slug']

    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        qs = qs.annotate(
            is_liked=RawSQL('select is_liked from "like" where book_id=book.id and user_id=%s',
                            (user.id,)))  # noqa
        qs = qs.annotate(
            is_favourite=RawSQL('select is_favourite from "favourite" where book_id=book.id and user_id=%s',
                            (user.id,)))  # noqa
        return qs

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        book = self.get_object()
        user = request.user

        obj, _ = Like.objects.get_or_create(user=user, book=book)
        obj.like()
        return Response({'book_status': 'liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def dislike(self, request, pk=None):
        book = self.get_object()
        user = request.user

        obj, _ = Like.objects.get_or_create(user=user, book=book)
        obj.dislike()
        return Response({'book_status': 'disliked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def deactivate(self, request, pk=None):
        book = self.get_object()
        user = request.user

        obj, _ = Like.objects.get_or_create(user=user, book=book)
        obj.deactivate()
        return Response({'book_status': 'deactivate'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def favour(self, request, pk=None):
        book = self.get_object()
        user = request.user

        obj, _ = Favourite.objects.get_or_create(user=user, book=book)
        obj.favourite()
        return Response({'book_status': 'favourite'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unfavour(self, request, pk=None):
        book = self.get_object()
        user = request.user

        obj, _ = Favourite.objects.get_or_create(user=user, book=book)
        obj.unfavourite()
        return Response({'book_status': 'not_favourite'}, status=status.HTTP_200_OK)

from django.db.models.expressions import RawSQL
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Api.permissions import IsSuperuserPermission
from Api.filters import BaseCrmFilter
from Api.serializers import EmptySerializer
from core.Book.models import Book
from core.Like.models import Like
from core.Favourite.models import Favourite
from .serializers import BookSerializer, BookViewSerializer, BookCreateUpdateSerializer


class BookFilter(BaseCrmFilter):
    class Meta:
        model = Book
        fields = ['is_active', 'author', 'category']


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperuserPermission]

    queryset = Book.objects.select_related('author').prefetch_related('category').all()
    serializer_class = BookSerializer
    serializer_map = {
        'list': BookViewSerializer,
        'retrieve': BookViewSerializer,
        'create': BookCreateUpdateSerializer,
        'update': BookCreateUpdateSerializer,
    }
    empty_serializer_set = {'archive', 'restore', 'like', 'dislike', 'deactivate', 'favour', 'unfavour'}
    ordering_fields = ['publish_date']
    search_fields = ['name', 'author__name']
    filterset_class = BookFilter

    def get_serializer_class(self):
        if self.action in self.empty_serializer_set:
            return EmptySerializer
        return self.serializer_map.get(self.action, self.serializer_class)

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

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.archive(user)

        data = self.serializer_class(obj).data
        return Response({'book': data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.restore(user)

        data = self.serializer_class(obj).data
        return Response({'book': data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        book = self.get_object()
        user = request.user

        obj, _ = Like.objects.get_or_create(user=user, book=book)
        obj.like()

        data = self.serializer_class(book).data
        return Response({'book': data, 'book_status': 'liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        book = self.get_object()
        user = request.user

        obj, _ = Like.objects.get_or_create(user=user, book=book)
        obj.dislike()

        data = self.serializer_class(book).data
        return Response({'book': data, 'book_status': 'disliked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        book = self.get_object()
        user = request.user

        obj, _ = Like.objects.get_or_create(user=user, book=book)
        obj.deactivate()

        data = self.serializer_class(book).data
        return Response({'book': data, 'book_status': 'deactivate'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def favour(self, request, pk=None):
        book = self.get_object()
        user = request.user

        obj, _ = Favourite.objects.get_or_create(user=user, book=book)
        obj.favourite()

        data = self.serializer_class(book).data
        return Response({'book': data, 'book_status': 'favourite'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unfavour(self, request, pk=None):
        book = self.get_object()
        user = request.user

        obj, _ = Favourite.objects.get_or_create(user=user, book=book)
        obj.unfavourite()

        data = self.serializer_class(book).data
        return Response({'book': data, 'book_status': 'not_favourite'}, status=status.HTTP_200_OK)

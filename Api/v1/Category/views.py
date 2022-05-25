from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Api.permissions import IsSuperuserPermission
from Api.filters import BaseCrmFilter
from Api.serializers import EmptySerializer
from core.Category.models import Category
from Api.v1.Book.serializers import BookArchiveSerializer
from .serializers import CategorySerializer, CategoryViewSerializer, CategoryArchiveSerializer


class CategoryFilter(BaseCrmFilter):
    class Meta:
        model = Category
        fields = ['is_active']


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperuserPermission]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    serializer_map = {
        'list': CategoryViewSerializer,
        'retrieve': CategoryViewSerializer,
    }
    empty_serializer_set = {'archive', 'restore'}

    category_archive_serializer_class = CategoryArchiveSerializer
    book_archive_serializer_class = BookArchiveSerializer

    ordering_fields = ['name']
    search_fields = ['name', 'slug']
    filterset_class = CategoryFilter

    def get_serializer_class(self):
        if self.action in self.empty_serializer_set:
            return EmptySerializer
        return self.serializer_map.get(self.action, self.serializer_class)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.archive(user)

        books = obj.book_set.all()
        books.archive(user)

        category_data = self.category_archive_serializer_class(obj).data
        books_data = self.book_archive_serializer_class(books, many=True).data
        return Response({'category': category_data, 'books': books_data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.restore(user)

        books = obj.book_set.all()
        books.restore(user)

        category_data = self.category_archive_serializer_class(obj).data
        books_data = self.book_archive_serializer_class(books, many=True).data
        return Response({'category': category_data, 'books': books_data}, status=status.HTTP_200_OK)

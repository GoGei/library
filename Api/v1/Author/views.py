from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Api.v1.Book.serializers import BookArchiveSerializer
from Api.permissions import IsSuperuserPermission
from Api.filters import BaseCrmFilter
from Api.serializers import EmptySerializer
from core.Author.models import Author
from .serializers import AuthorSerializer, AuthorViewSerializer


class AuthorFilter(BaseCrmFilter):
    class Meta:
        model = Author
        fields = ['is_active']


class AuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperuserPermission]

    queryset = Author.objects.all().ordered()
    serializer_class = AuthorSerializer
    serializer_map = {
        'list': AuthorViewSerializer,
        'retrieve': AuthorViewSerializer,
    }

    book_archive_serializer_class = BookArchiveSerializer

    empty_serializer_set = {'archive', 'restore'}
    ordering_fields = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name', 'middle_name']
    filterset_class = AuthorFilter

    def get_serializer_class(self):
        if self.action in self.empty_serializer_set:
            return EmptySerializer
        return self.serializer_map.get(self.action, self.serializer_class)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        books = instance.book_set.all()
        if books.exists():
            id_lst = [str(e) for e in books.values_list('id', flat=True).distinct()]
            return Response({'model_protect_restriction': 'To this author bound books! (%s)' % ','.join(id_lst)},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.archive(user)

        books = obj.book_set.all()
        books.archive(user)

        author_data = self.serializer_class(obj).data
        books_data = self.book_archive_serializer_class(books, many=True).data
        return Response({'author': author_data, 'books': books_data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.restore(user)

        books = obj.book_set.all()
        books.restore(user)

        author_data = self.serializer_class(obj).data
        books_data = self.book_archive_serializer_class(books, many=True).data
        return Response({'author': author_data, 'books': books_data}, status=status.HTTP_200_OK)

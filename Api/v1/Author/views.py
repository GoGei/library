from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Api.filters import BaseCrmFilter
from core.Author.models import Author
from .serializers import AuthorSerializer, AuthorViewSerializer


class AuthorFilter(BaseCrmFilter):
    class Meta:
        model = Author
        fields = ['is_active']


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().ordered()
    serializer_class = AuthorSerializer
    serializer_map = {
        'list': AuthorViewSerializer,
        'retrieve': AuthorViewSerializer,
    }
    ordering_fields = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name', 'middle_name']
    filterset_class = AuthorFilter

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.archive(user)

        books = obj.book_set.all()
        books.archive(user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.restore(user)

        books = obj.book_set.all()
        books.restore(user)
        return Response(status=status.HTTP_200_OK)

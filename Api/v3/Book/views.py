from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import AdminRenderer

from Api.permissions import IsStaffPermission
from Api.filters import BaseCrmFilter
from core.Book.models import Book
from .serializers import BookSerializer, BookListSerializer, BookRetrieveSerializer, BookCreateUpdateSerializer


class BookFilter(BaseCrmFilter):
    class Meta:
        model = Book
        fields = ['is_active', 'author', 'category']


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffPermission]
    renderer_classes = [AdminRenderer]

    queryset = Book.objects.select_related('author').prefetch_related('category').all()
    serializer_class = BookSerializer
    serializer_map = {
        'list': BookListSerializer,
        'retrieve': BookRetrieveSerializer,
        'create': BookCreateUpdateSerializer,
        'update': BookCreateUpdateSerializer,
    }
    ordering_fields = ['publish_date']
    search_fields = ['name', 'author__name']
    filterset_class = BookFilter

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.archive(user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.restore(user)
        return Response(status=status.HTTP_200_OK)

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Api.filters import BaseCrmFilter
from core.Category.models import Category
from .serializers import CategorySerializer


class CategoryFilter(BaseCrmFilter):
    class Meta:
        model = Category
        fields = ['is_active']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    ordering_fields = ['name']
    search_fields = ['name', 'slug']
    filterset_class = CategoryFilter

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

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import AdminRenderer

from Api.permissions import IsStaffPermission
from Api.filters import BaseCrmFilter
from Api.serializers import EmptySerializer
from core.Category.models import Category
from .serializers import CategorySerializer, CategoryListSerializer, CategoryRetrieveSerializer


class CategoryFilter(BaseCrmFilter):
    class Meta:
        model = Category
        fields = ['is_active']


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffPermission]
    renderer_classes = [AdminRenderer]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    serializer_map = {
        'list': CategoryListSerializer,
        'retrieve': CategoryRetrieveSerializer,
    }
    empty_serializer_set = {'archive', 'restore'}
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
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.restore(user)

        books = obj.book_set.all()
        books.restore(user)
        return Response(status=status.HTTP_200_OK)

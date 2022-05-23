from rest_framework import viewsets, permissions
from core.Category.models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.active().all()
    serializer_class = CategorySerializer

    filterset_fields = []
    ordering_fields = ['name']
    search_fields = ['name', 'slug']

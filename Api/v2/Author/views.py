from rest_framework import viewsets, permissions
from core.Author.models import Author
from .serializers import AuthorSerializer


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Author.objects.active().all()
    serializer_class = AuthorSerializer

    filterset_fields = []
    ordering_fields = ['id', 'first_name', 'last_name']
    search_fields = ['first_name', 'last_name']

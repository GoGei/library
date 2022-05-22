from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.Author.models import Author
from .serializers import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

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

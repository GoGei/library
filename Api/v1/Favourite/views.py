from rest_framework import viewsets

from .serializers import FavouriteSerializer, FavouriteViewSerializer
from core.Favourite.models import Favourite


class FavouriteViewSet(viewsets.ModelViewSet):
    queryset = Favourite.objects.select_related('user', 'book').all()
    serializer_class = FavouriteSerializer
    serializer_map = {
        'list': FavouriteViewSerializer,
        'retrieve': FavouriteViewSerializer,
    }
    ordering_fields = []
    search_fields = ['user__email', 'book__name']
    filterset_fields = ['is_liked']

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

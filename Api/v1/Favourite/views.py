from rest_framework import viewsets

from Api.permissions import IsSuperuserPermission
from core.Favourite.models import Favourite
from .serializers import FavouriteSerializer, FavouriteViewSerializer


class FavouriteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperuserPermission]

    queryset = Favourite.objects.select_related('user', 'book').all()
    serializer_class = FavouriteSerializer
    serializer_map = {
        'list': FavouriteViewSerializer,
        'retrieve': FavouriteViewSerializer,
    }
    ordering_fields = []
    search_fields = ['user__email', 'book__name']
    filterset_fields = ['is_favourite']

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

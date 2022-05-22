from rest_framework import viewsets

from .serializers import LikeSerializer, LikeViewSerializer
from core.Like.models import Like


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.select_related('user', 'book').all()
    serializer_class = LikeSerializer
    serializer_map = {
        'list': LikeViewSerializer,
        'retrieve': LikeViewSerializer,
    }
    ordering_fields = []
    search_fields = ['user__email', 'book__name']
    filterset_fields = ['is_liked']

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

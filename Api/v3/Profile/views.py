from rest_framework import viewsets
from rest_framework.renderers import AdminRenderer

from Api.permissions import IsStaffPermission
from core.Profile.models import Profile
from Api.serializers import EmptySerializer
from .serializers import ProfileViewSerializer, ProfileSerializer


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsStaffPermission]
    renderer_classes = [AdminRenderer]

    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    serializer_map = {
        'list': ProfileViewSerializer,
        'retrieve': ProfileViewSerializer,
    }
    empty_serializer_set = {}

    def get_serializer_class(self):
        if self.action in self.empty_serializer_set:
            return EmptySerializer
        return self.serializer_map.get(self.action, self.serializer_class)

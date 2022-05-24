from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.Profile.models import Profile
from core.User.models import User
from Api.serializers import EmptySerializer
from Api.v3.User.serializers import UserProfileSerializer
from .serializers import ProfileViewSerializer, ProfileSerializer


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    serializer_map = {
        'list': ProfileViewSerializer,
        'retrieve': ProfileViewSerializer,
        'set_to_user': UserProfileSerializer,
    }
    empty_serializer_set = {}

    def get_serializer_class(self):
        if self.action in self.empty_serializer_set:
            return EmptySerializer
        return self.serializer_map.get(self.action, self.serializer_class)

    @action(detail=True, methods=['post'])
    def set_to_user(self, request, pk=None):
        pass

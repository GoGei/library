from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.User.models import User
from Api.serializers import EmptySerializer
from Api.v3.Profile.serializers import ProfileUserSerializer
from .serializers import UserListSerializer, UserRetrieveSerializer, UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.prefetch_related('profile_set', 'like_set', 'favourite_set').all()
    serializer_class = UserSerializer
    serializer_map = {
        'list': UserListSerializer,
        'retrieve': UserRetrieveSerializer,
        'profiles': ProfileUserSerializer,
    }
    empty_serializer_set = {}

    def get_serializer_class(self):
        if self.action in self.empty_serializer_set:
            return EmptySerializer
        return self.serializer_map.get(self.action, self.serializer_class)

    @action(detail=True, methods=['get'])
    def profiles(self, request, pk=None):
        user = self.get_object()
        queryset = user.profile_set.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

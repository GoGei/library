from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Api.v1.Profile.serializers import ProfileArchiveSerializer
from Api.permissions import IsSuperuserPermission
from Api.serializers import EmptySerializer
from core.User.models import User
from .serializers import UserSerializer, UserListSerializer, UserCreateUpdateSerializer, UserSetPasswordSerializer, \
    UserArchiveSerializer, UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperuserPermission]

    queryset = User.objects.prefetch_related('profile_set', 'like_set', 'favourite_set').all()
    serializer_class = UserSerializer
    serializer_map = {
        'list': UserListSerializer,
        'create': UserCreateUpdateSerializer,
        'update': UserCreateUpdateSerializer,
        'set_password': UserSetPasswordSerializer,
        'profiles': UserProfileSerializer
    }
    user_archive_serializer = UserArchiveSerializer
    profile_archive_serializer = ProfileArchiveSerializer

    empty_serializer_set = {'archive', 'restore'}
    ordering_fields = ['email']
    search_fields = ['email']
    filterset_fields = ['is_active', 'is_staff', 'is_superuser']

    def get_serializer_class(self):
        if self.action in self.empty_serializer_set:
            return EmptySerializer
        return self.serializer_map.get(self.action, self.serializer_class)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.archive()

        profiles = obj.profile_set.all()
        profiles.archive(user)

        user_data = self.user_archive_serializer(obj).data
        profile_data = self.profile_archive_serializer(profiles, many=True).data
        return Response({'user': user_data, 'profiles': profile_data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.restore()

        profiles = obj.profile_set.all()
        profiles.restore(user)

        user_data = self.user_archive_serializer(obj).data
        profile_data = self.profile_archive_serializer(profiles, many=True).data
        return Response({'user': user_data, 'profiles': profile_data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='set-password')
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def profiles(self, request, pk=None):
        user = self.get_object()
        profiles = user.profile_set.all().ordered()
        serializer = self.get_serializer(profiles, many=True)
        return Response(data=serializer.data)

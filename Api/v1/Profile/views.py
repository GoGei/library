from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Api.permissions import IsSuperuserPermission
from Api.filters import BaseCrmFilter
from Api.serializers import EmptySerializer
from core.Profile.models import Profile
from core.User.models import User
from .serializers import ProfileSerializer, ProfileListSerializer, ProfileCreateWithUser, ProfileDetailSerializer


class ProfileFilter(BaseCrmFilter):
    class Meta:
        model = Profile
        fields = ['is_active', 'is_banned']


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperuserPermission]

    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    serializer_map = {
        'list': ProfileListSerializer,
        'retrieve': ProfileDetailSerializer,
        'create_with_user': ProfileCreateWithUser,
    }
    empty_serializer_set = {'archive', 'restore'}
    ordering_fields = []
    search_fields = ['user__email']
    filterset_class = ProfileFilter

    def get_serializer_class(self):
        if self.action in self.empty_serializer_set:
            return EmptySerializer
        return self.serializer_map.get(self.action, self.serializer_class)

    @action(detail=False, methods=['post'], url_path='create-with-user')
    def create_with_user(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = User.objects.create_user(**data)
            profile = Profile(user=user)
            profile.save()
            return Response(ProfileListSerializer(profile).data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.archive(user)

        data = self.serializer_class(obj).data
        return Response({'profile': data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.restore(user)

        data = self.serializer_class(obj).data
        return Response({'profile': data}, status=status.HTTP_200_OK)

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.Profile.models import Profile
from core.User.models import User
from Api.v1.filters import BaseCrmFilter
from .serializers import ProfileSerializer, ProfileListSerializer, \
    ProfileCreateWithUser, ProfileDetailSerializer


class ProfileFilter(BaseCrmFilter):
    class Meta:
        model = Profile
        fields = ['is_active']


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    serializer_map = {
        'list': ProfileListSerializer,
        'retrieve': ProfileDetailSerializer,
        'create_with_user': ProfileCreateWithUser,
    }

    ordering_fields = []
    search_fields = ['user__email']
    filterset_class = ProfileFilter

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    @action(detail=False, methods=['post'], url_path='create-with-user')
    def create_with_user(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            user = User.objects.create_user(email=data['email'], password=None)
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
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.restore(user)
        return Response(status=status.HTTP_200_OK)

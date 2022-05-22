from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserSerializer, UserListSerializer, UserCreateUpdateSerializer, UserSetPasswordSerializer

from core.User.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related('profile_set').all()
    serializer_class = UserSerializer
    serializer_map = {
        'list': UserListSerializer,
        'create': UserCreateUpdateSerializer,
        'update': UserCreateUpdateSerializer,
        'set_password': UserSetPasswordSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.archive(user)

        profiles = obj.profile_set.all()
        profiles.archive(user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        obj.restore(user)

        profiles = obj.profile_set.all()
        profiles.restore(user)
        return Response(status=status.HTTP_200_OK)

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

from rest_framework import serializers
from Api.v1.Users.serializers import UserSerializer
from core.Profile.models import Profile
from core.User.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user']


class ProfileListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user']
        read_only = ['id']


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user']
        read_only = ['id', 'user']


class ProfileCreateWithUser(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, data):
        try:
            User.objects.get(email=data['email'])
            raise serializers.ValidationError({'email': ['User with this email is already exists!']})
        except User.DoesNotExist:
            # user with this email does not exists
            return data

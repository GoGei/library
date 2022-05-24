from rest_framework import serializers
from core.Profile.models import Profile
from Api.v3.User.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'is_banned', 'expire_date']


class ProfileViewSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'is_banned', 'expire_date']


class ProfileUserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'expire_date']
        read_only_fields = ['id']


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'is_banned', 'expire_date']

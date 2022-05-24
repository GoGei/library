from rest_framework import serializers
from core.User.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'first_name', 'last_name', 'middle_name']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'first_name', 'last_name', 'middle_name']


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'first_name', 'last_name', 'middle_name']


class UserProfileSerializer(serializers.Serializer):
    pass

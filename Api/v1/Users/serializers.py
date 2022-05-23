from rest_framework import serializers
from core.User.models import User
from core.Utils.validators import PasswordValidator
from Api.v1.serializers import BaseCreateUpdateSerializer


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserCreateUpdateSerializer(BaseCreateUpdateSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'is_staff', 'is_superuser']
        read_only_fields = ['id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'is_staff', 'is_superuser']


class UserSetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=32, required=True, write_only=True,
                                     style={'input_type': 'password'}, validators=[PasswordValidator])
    repeat_password = serializers.CharField(min_length=8, max_length=32, required=True, write_only=True,
                                            style={'input_type': 'password'}, validators=[PasswordValidator])

    class Meta:
        fields = ['password', 'repeat_password']

    def validate(self, data):
        if data['password'] != data['repeat_password']:
            raise serializers.ValidationError('Password mismatch!')
        return data


class UserCrmSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

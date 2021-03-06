from rest_framework import serializers
from core.User.models import User
from core.Profile.models import Profile
from core.Utils.validators import PasswordValidator


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'is_staff', 'is_superuser', 'first_name', 'last_name', 'middle_name']
        read_only_fields = ['id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'is_staff', 'is_superuser', 'first_name', 'last_name', 'middle_name']


class UserSetPasswordSerializer(serializers.Serializer):
    disable_complex_password = serializers.BooleanField(required=False, default=False)
    password = serializers.CharField(min_length=8, max_length=32, required=True, write_only=True)
    repeat_password = serializers.CharField(min_length=8, max_length=32, required=True, write_only=True)

    class Meta:
        fields = ['password', 'repeat_password', 'disable_complex_password']

    def validate(self, data):
        password = data['password']
        repeat_password = data['repeat_password']
        if not data['disable_complex_password']:
            PasswordValidator(password)
            PasswordValidator(repeat_password)

        if password != repeat_password:
            raise serializers.ValidationError('Password mismatch!')
        return data


class UserCrmSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class UserArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_staff', 'is_superuser', 'first_name', 'last_name', 'middle_name']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'is_banned', 'expire_date']

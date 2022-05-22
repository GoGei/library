from rest_framework import serializers
from core.User.models import User
from core.Utils.validators import PasswordValidator


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'is_staff', 'is_superuser']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        instance = super(UserCreateUpdateSerializer, self).update(instance, validated_data)
        instance.modify(self.context['request'].user)
        return instance


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

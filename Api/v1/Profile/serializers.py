from rest_framework import serializers
from Api.v1.Users.serializers import UserSerializer, UserCrmSerializer
from Api.serializers import BaseCreateUpdateSerializer
from core.Profile.models import Profile
from core.User.models import User
from core.Utils.validators import PasswordValidator


class ProfileListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    created_by = UserCrmSerializer()
    modified_by = UserCrmSerializer()
    archived_by = UserCrmSerializer()

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileSerializer(BaseCreateUpdateSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user']
        read_only_fields = ['id']


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user']


class ProfileCreateWithUser(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    middle_name = serializers.CharField(max_length=50, required=False)

    disable_complex_password = serializers.BooleanField(required=False, default=False)
    password = serializers.CharField(min_length=8, max_length=32, required=True, write_only=True)
    repeat_password = serializers.CharField(min_length=8, max_length=32, required=True, write_only=True)

    def validate(self, data):
        try:
            User.objects.get(email=data['email'])
            raise serializers.ValidationError({'email': ['User with this email is already exists!']})
        except User.DoesNotExist:
            # user with this email does not exists
            pass

        password = data['password']
        repeat_password = data['repeat_password']
        if not data['disable_complex_password']:
            PasswordValidator(password)
            PasswordValidator(repeat_password)

        if password != repeat_password:
            raise serializers.ValidationError('Password mismatch!')

        excluded_fields = ['disable_complex_password', 'repeat_password']
        [data.pop(key) for key in excluded_fields]
        return data

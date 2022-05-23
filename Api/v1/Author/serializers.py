from rest_framework import serializers
from core.Author.models import Author
from Api.v1.Users.serializers import UserCrmSerializer
from Api.v1.serializers import BaseCreateUpdateSerializer


class AuthorSerializer(BaseCreateUpdateSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'middle_name']
        read_only_fields = ['id']


class AuthorViewSerializer(serializers.ModelSerializer):
    created_by = UserCrmSerializer()
    modified_by = UserCrmSerializer()
    archived_by = UserCrmSerializer()

    class Meta:
        model = Author
        fields = '__all__'

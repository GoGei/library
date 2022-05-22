from rest_framework import serializers
from core.Author.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'middle_name']
        read_only_fields = ['id']


class AuthorViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'label', 'is_active', 'first_name', 'last_name', 'middle_name']
        read_only_fields = ['id', 'label', 'is_active']

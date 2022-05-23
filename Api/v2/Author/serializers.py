from rest_framework import serializers
from core.Author.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'middle_name']
        ref_name = 'Author for users (v2)'

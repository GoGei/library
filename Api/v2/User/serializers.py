from rest_framework import serializers
from core.Book.models import Book
from Api.v2.Author.serializers import AuthorSerializer
from Api.v2.Category.serializers import CategorySerializer


class BookProfileSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['id', 'name', 'slug', 'description', 'category', 'author', 'publish_date']


class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    middle_name = serializers.CharField()
    liked = BookProfileSerializer(many=True)
    favourite = BookProfileSerializer(many=True)
    is_banned = serializers.NullBooleanField(source='profile.is_banned')

    class Meta:
        fields = ['id', 'email', 'is_banned', 'first_name', 'last_name', 'middle_name', 'liked', 'favourite']

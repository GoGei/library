from rest_framework import serializers
from core.Book.models import Book
from Api.v2.Author.serializers import AuthorSerializer
from Api.v2.Category.serializers import CategorySerializer


class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    author = AuthorSerializer()
    is_liked = serializers.NullBooleanField()
    is_favourite = serializers.BooleanField()

    class Meta:
        model = Book
        fields = ['id', 'name', 'slug', 'description', 'category', 'author', 'publish_date', 'is_liked', 'is_favourite']
        ref_name = 'Book for users (v2)'

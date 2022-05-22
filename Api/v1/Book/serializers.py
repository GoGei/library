from rest_framework import serializers
from core.Book.models import Book
from Api.v1.Category.serializers import CategorySerializer
from Api.v1.Author.serializers import AuthorSerializer


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'category', 'author', 'publish_date']
        read_only_fields = ['id']


class BookViewSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = '__all__'


class BookRelatedObjectsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['id', 'name', 'category', 'author', 'publish_date']

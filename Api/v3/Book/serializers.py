from rest_framework import serializers
from core.Book.models import Book
from Api.serializers import BaseCreateUpdateSerializer, BaseCrmSerializer, BaseUrlObjectSerializer, STAMP_FORMAT


class BookSerializer(serializers.ModelSerializer):
    publish_date = serializers.DateField(format=STAMP_FORMAT)

    class Meta:
        model = Book
        fields = ['id', 'name', 'category', 'author', 'publish_date']
        read_only_fields = ['id']


class BookCreateUpdateSerializer(BaseCreateUpdateSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'category', 'author', 'publish_date', 'description']
        read_only_fields = ['id']

    def validate(self, data):
        instance = self.instance
        if not Book.is_allowed_to_assign_slug(data['name'], instance):
            raise serializers.ValidationError({'name': ['This name cause slug duplication!']})
        return data

    def create(self, validated_data):
        instance = super(BookCreateUpdateSerializer, self).create(validated_data)
        instance.assign_slug()
        return instance

    def update(self, instance, validated_data):
        instance = super(BookCreateUpdateSerializer, self).update(instance, validated_data)
        instance.assign_slug()
        return instance


class BookBaseSerializer(serializers.ModelSerializer):
    publish_date = serializers.DateField(format=STAMP_FORMAT)
    category = serializers.StringRelatedField(many=True)
    author = serializers.StringRelatedField()


class BookListSerializer(BaseUrlObjectSerializer, BookBaseSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'category', 'author', 'publish_date', 'is_active', 'url']


class BookRetrieveSerializer(BaseCrmSerializer, BookBaseSerializer):
    class Meta:
        model = Book
        fields = '__all__'

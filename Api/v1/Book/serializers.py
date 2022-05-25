from rest_framework import serializers
from core.Book.models import Book
from Api.v1.Category.serializers import CategorySerializer
from Api.v1.Author.serializers import AuthorSerializer
from Api.v1.Users.serializers import UserCrmSerializer
from Api.serializers import BaseCreateUpdateSerializer, STAMP_FORMAT


class BookSerializer(serializers.ModelSerializer):
    publish_date = serializers.DateField(format=STAMP_FORMAT)

    class Meta:
        model = Book
        fields = ['id', 'name', 'slug', 'category', 'author', 'publish_date']
        read_only_fields = ['id', 'slug']


class BookCreateUpdateSerializer(BaseCreateUpdateSerializer):
    class Meta:
        model = Book
        fields = ['id', 'slug', 'name', 'category', 'author', 'publish_date', 'description']
        read_only_fields = ['id', 'slug']

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


class BaseBookSerializer(serializers.ModelSerializer):
    publish_date = serializers.DateField(format=STAMP_FORMAT)
    category = CategorySerializer(many=True)
    author = AuthorSerializer()


class BookViewSerializer(BaseBookSerializer):
    created_by = UserCrmSerializer()
    modified_by = UserCrmSerializer()
    archived_by = UserCrmSerializer()

    is_liked = serializers.NullBooleanField()
    is_favourite = serializers.BooleanField()

    class Meta:
        model = Book
        fields = '__all__'
        extra_fields = ['is_liked', 'is_favourite']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(BookViewSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class BookRelatedObjectsSerializer(BaseBookSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'category', 'author', 'publish_date']


class BookArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'slug', 'name']

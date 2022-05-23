from rest_framework import serializers
from core.Book.models import Book
from Api.v1.Category.serializers import CategorySerializer
from Api.v1.Author.serializers import AuthorSerializer
from Api.v1.Users.serializers import UserCrmSerializer
from Api.v1.serializers import BaseCreateUpdateSerializer


class BookSerializer(BaseCreateUpdateSerializer):
    publish_date = serializers.DateField()

    class Meta:
        model = Book
        fields = ['id', 'name', 'category', 'author', 'publish_date']
        read_only_fields = ['id']

    def validate(self, data):
        instance = self.instance
        if not Book.is_allowed_to_assign_slug(data['name'], instance):
            raise serializers.ValidationError({'name': ['This name cause slug duplication!']})
        return data

    def create(self, validated_data):
        instance = super(BookSerializer, self).create(validated_data)
        instance.assign_slug()
        return instance

    def update(self, instance, validated_data):
        instance = super(BookSerializer, self).update(instance, validated_data)
        instance.assign_slug()
        return instance


class BookViewSerializer(serializers.ModelSerializer):
    publish_date = serializers.DateField()

    category = CategorySerializer(many=True)
    author = AuthorSerializer()
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


class BookRelatedObjectsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['id', 'name', 'category', 'author', 'publish_date']

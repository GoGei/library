from rest_framework import serializers
from core.Category.models import Category
from Api.v1.Users.serializers import UserCrmSerializer
from Api.serializers import BaseCreateUpdateSerializer


class CategorySerializer(BaseCreateUpdateSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'label', 'is_active']
        read_only_fields = ['id', 'slug', 'label', 'is_active']

    def validate(self, data):
        instance = self.instance
        if not Category.is_allowed_to_assign_slug(data['name'], instance):
            raise serializers.ValidationError({'name': ['This name cause slug duplication!']})
        return data

    def create(self, validated_data):
        instance = super(CategorySerializer, self).create(validated_data)
        instance.assign_slug()
        return instance

    def update(self, instance, validated_data):
        instance = super(CategorySerializer, self).update(instance, validated_data)
        instance.assign_slug()
        return instance


class CategoryViewSerializer(serializers.ModelSerializer):
    created_by = UserCrmSerializer()
    modified_by = UserCrmSerializer()
    archived_by = UserCrmSerializer()

    class Meta:
        model = Category
        fields = '__all__'


class CategoryArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

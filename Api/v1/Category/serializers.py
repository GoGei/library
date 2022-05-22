from rest_framework import serializers
from core.Category.models import Category


class CategorySerializer(serializers.ModelSerializer):
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

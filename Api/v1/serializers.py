from rest_framework import serializers


class BaseCreateUpdateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = super(BaseCreateUpdateSerializer, self).create(validated_data)
        instance.created_by = self.context['request'].user
        return instance

    def update(self, instance, validated_data):
        instance = super(BaseCreateUpdateSerializer, self).update(instance, validated_data)
        instance.modify(self.context['request'].user)
        return instance

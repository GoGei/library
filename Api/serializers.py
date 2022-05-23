from rest_framework import serializers

STAMP_FORMAT = '%d %b %Y'


class EmptySerializer(serializers.Serializer):
    # created for actions that not require body
    pass


class BaseCreateUpdateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = super(BaseCreateUpdateSerializer, self).create(validated_data)
        instance.created_by = self.context['request'].user
        return instance

    def update(self, instance, validated_data):
        instance = super(BaseCreateUpdateSerializer, self).update(instance, validated_data)
        instance.modify(self.context['request'].user)
        return instance


class BaseCrmSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    archived_by = serializers.StringRelatedField()

    created_stamp = serializers.DateTimeField(format=STAMP_FORMAT)
    modified_stamp = serializers.DateTimeField(format=STAMP_FORMAT)
    archived_stamp = serializers.DateTimeField(format=STAMP_FORMAT)


class BaseUrlObjectSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True, method_name='get_detail_url')

    def get_detail_url(self, obj):
        request = self.context['request']
        url = '%s%s/' % (request.path, obj.id)
        return url

from rest_framework import serializers
from core.Like.models import Like
from Api.v1.Users.serializers import UserSerializer
from Api.v1.Book.serializers import BookRelatedObjectsSerializer


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class LikeViewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    book = BookRelatedObjectsSerializer()

    class Meta:
        model = Like
        fields = '__all__'

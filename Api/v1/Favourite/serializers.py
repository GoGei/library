from rest_framework import serializers
from core.Favourite.models import Favourite
from Api.v1.Users.serializers import UserSerializer
from Api.v1.Book.serializers import BookRelatedObjectsSerializer


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'


class FavouriteViewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    book = BookRelatedObjectsSerializer()

    class Meta:
        model = Favourite
        fields = '__all__'

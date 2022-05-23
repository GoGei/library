from rest_framework import serializers
from core.Profile.models import Profile
from core.Book.models import Book
from Api.v2.Author.serializers import AuthorSerializer
from Api.v2.Category.serializers import CategorySerializer


class BookProfileSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['id', 'name', 'slug', 'description', 'category', 'author', 'publish_date']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['is_banned']


class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    liked = BookProfileSerializer(many=True)
    favourite = BookProfileSerializer(many=True)
    profile = UserProfileSerializer()

    class Meta:
        fields = ['id', 'email', 'liked', 'favourite', 'profile']

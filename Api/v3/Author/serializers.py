from core.Author.models import Author
from Api.serializers import BaseCreateUpdateSerializer, BaseCrmSerializer, BaseUrlObjectSerializer


class AuthorSerializer(BaseCreateUpdateSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'middle_name']
        read_only_fields = ['id']


class AuthorListSerializer(BaseUrlObjectSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'is_active', 'url']


class AuthorRetrieveSerializer(BaseCrmSerializer):
    class Meta:
        model = Author
        fields = '__all__'

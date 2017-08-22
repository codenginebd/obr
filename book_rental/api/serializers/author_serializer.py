from book_rental.models.author import Author
from generics.api.serializers.base_model_serializer import BaseModelSerializer


class AuthorSerializer(BaseModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'code', 'name', 'date_created', 'last_updated')
from book_rental.models.language import BookLanguage
from generics.api.serializers.base_model_serializer import BaseModelSerializer


class BookLanguageSerializer(BaseModelSerializer):
    class Meta:
        model = BookLanguage
        fields = ('id', 'code', 'name', 'short_name', 'date_created', 'last_updated')

from book_rental.models.book_publisher import BookPublisher
from generics.api.serializers.base_model_serializer import BaseModelSerializer


class PublisherSerializer(BaseModelSerializer):
    class Meta:
        model = BookPublisher
        fields = ('id', 'code', 'name', 'date_created', 'last_updated')
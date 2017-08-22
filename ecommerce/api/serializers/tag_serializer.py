from ecommerce.models.sales.keyword import TagKeyword
from generics.api.serializers.base_model_serializer import BaseModelSerializer


class TagSerializer(BaseModelSerializer):
    class Meta:
        model = TagKeyword
        fields = ('id', 'code', 'name', 'date_created', 'last_updated')

from ecommerce.models.sales.category import ProductCategory
from generics.api.serializers.base_model_serializer import BaseModelSerializer


class CategorySerializer(BaseModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ('id', 'code', 'name', 'parent_id', 'date_created', 'last_updated')
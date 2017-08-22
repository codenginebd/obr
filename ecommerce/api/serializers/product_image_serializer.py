from ecommerce.models.sales.product_images import ProductImage
from generics.api.serializers.base_model_serializer import BaseModelSerializer


class ProductImageSerializer(BaseModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'code', 'image', 'thumbnail', 'date_created', 'last_updated')

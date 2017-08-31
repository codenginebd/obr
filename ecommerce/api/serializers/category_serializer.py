from django.core.urlresolvers import reverse
from ecommerce.models.sales.category import ProductCategory
from generics.api.serializers.base_model_serializer import BaseModelSerializer
from rest_framework import serializers

class CategorySerializer(BaseModelSerializer):
    link = serializers.SerializerMethodField()
    
    def get_link(self, obj):
        return ""

    class Meta:
        model = ProductCategory
        fields = ('id', 'code', 'name', 'link', 'parent_id', 'date_created', 'last_updated')
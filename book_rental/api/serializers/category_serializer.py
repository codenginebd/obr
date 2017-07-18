from rest_framework import serializers
from generics.models.sales.category import ProductCategory


class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'code', 'name', 'parent_id', 'date_created', 'last_updated')

from rest_framework import serializers
from book.models.category import BookCategory


class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = ('id', 'code', 'name', 'parent_id', 'date_created', 'last_updated')

from rest_framework import serializers
from book.models.category import BookCategory


class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = ('id', 'name')

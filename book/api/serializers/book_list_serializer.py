from rest_framework import serializers
from book.models.book import Book


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'code', 'title', 'subtitle', 'description',
                  'category', 'is_active', 'date_created', 'last_updated')

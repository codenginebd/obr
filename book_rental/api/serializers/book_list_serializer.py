from rest_framework import serializers

from book_rental.api.serializers.author_serializer import AuthorSerializer
from book_rental.api.serializers.book_language_serializer import BookLanguageSerializer
from book_rental.api.serializers.publisher_serializer import PublisherSerializer
from book_rental.models.sales.book import Book
from ecommerce.api.serializers.category_serializer import CategorySerializer
from ecommerce.api.serializers.product_image_serializer import ProductImageSerializer
from ecommerce.api.serializers.tag_serializer import TagSerializer
from generics.api.serializers.base_model_serializer import BaseModelSerializer


class BookSerializer(BaseModelSerializer):
    categories = CategorySerializer(many=True, fields=[ 'id', 'code', 'name' ])
    tags = TagSerializer(many=True, fields=[ 'id', 'code', 'name' ])
    publisher = PublisherSerializer(fields=[ 'id', 'code', 'name', 'name_2' ])
    authors = AuthorSerializer(many=True, fields=[ 'id', 'code', 'name' ])
    language = BookLanguageSerializer(fields=[ 'id', 'code', 'name', 'short_name' ])
    images = ProductImageSerializer(many=True, fields=[ 'id', 'code', 'image', 'thumbnail' ])

    class Meta:
        model = Book
        fields = ('id', 'code', 'title', 'title_2', 'subtitle', 'subtitle_2', 'description', 'description_2', 'show_2',
                  'sale_available', 'page_count', 'categories', 'publisher', 'authors', 'tags', 'images',
                  'language', 'rent_available', 'slug', 'date_created', 'last_updated')

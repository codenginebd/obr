from book_rental.api.serializers.author_serializer import AuthorSerializer
from book_rental.api.serializers.book_language_serializer import BookLanguageSerializer
from book_rental.api.serializers.publisher_serializer import PublisherSerializer
from book_rental.models.sales.book import Book
from ecommerce.api.serializers.category_serializer import CategorySerializer
from ecommerce.api.serializers.product_image_serializer import ProductImageSerializer
from ecommerce.api.serializers.tag_serializer import TagSerializer
from ecommerce.models.sales.price_matrix import PriceMatrix
from generics.api.serializers.base_model_serializer import BaseModelSerializer
from rest_framework import serializers


class BookSerializer(BaseModelSerializer):
    categories = CategorySerializer(many=True, fields=[ 'id', 'code', 'name' ])
    tags = TagSerializer(many=True, fields=[ 'id', 'code', 'name' ])
    publisher = PublisherSerializer(fields=[ 'id', 'code', 'name', 'name_2' ])
    authors = AuthorSerializer(many=True, fields=[ 'id', 'code', 'name' ])
    language = BookLanguageSerializer(fields=[ 'id', 'code', 'name', 'short_name' ])
    images = ProductImageSerializer(many=True, fields=[ 'id', 'code', 'image', 'thumbnail' ])
    market_price = serializers.SerializerMethodField()

    def get_market_price(self, obj):
        price_matrix_objects = PriceMatrix.objects.filter(product_model=Book.__name__,
                                                          product_code=obj.code)\
            .values('market_price', 'base_price', 'currency__short_name', 'is_new', 'print_type', 'special_price')
        return price_matrix_objects[0]['market_price']

    class Meta:
        model = Book
        fields = ('id', 'code', 'title', 'title_2', 'subtitle', 'subtitle_2', 'description', 'description_2', 'show_2',
                  'sale_available', 'market_price', 'page_count', 'categories', 'publisher', 'authors', 'tags', 'images',
                  'language', 'rent_available', 'slug', 'date_created', 'last_updated')

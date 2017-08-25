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

from inventory.models.inventory import Inventory


class BookSerializer(BaseModelSerializer):
    categories = CategorySerializer(many=True, fields=[ 'id', 'code', 'name' ])
    tags = TagSerializer(many=True, fields=[ 'id', 'code', 'name' ])
    publisher = PublisherSerializer(fields=[ 'id', 'code', 'name', 'name_2' ])
    authors = AuthorSerializer(many=True, fields=[ 'id', 'code', 'name' ])
    language = BookLanguageSerializer(fields=[ 'id', 'code', 'name', 'short_name' ])
    images = ProductImageSerializer(many=True, fields=[ 'id', 'code', 'image', 'thumbnail' ])
    market_price = serializers.SerializerMethodField()
    base_price = serializers.SerializerMethodField()
    original_available = serializers.SerializerMethodField()
    color_available = serializers.SerializerMethodField()
    economy_available = serializers.SerializerMethodField()
    used_copy_available = serializers.SerializerMethodField()
    buy_options = serializers.SerializerMethodField()
    rent_options = serializers.SerializerMethodField()

    def get_buy_options(self, obj):
        inventory_objects = Inventory.objects.filter(product_model=Book.__name__,
                                                     product_id=obj.pk, stock__gt=0, is_new=1)
        options = []
        for inventory_object in inventory_objects:
            options += [
                {
                    "short_name": inventory_object.print_type,
                    "full_name": inventory_object.print_type_full_name
                }
            ]
        inventory_objects = Inventory.objects.filter(product_model=Book.__name__,
                                                     product_id=obj.pk, stock__gt=0, is_new=0)
        if inventory_objects.exists():
            options += [
                {
                    "short_name": "USED",
                    "full_name": "Used Copy"
                }
            ]
        return options

    def get_rent_options(self, obj):
        return []

    def get_original_available(self, obj):
        inventory_objects = Inventory.objects.filter(product_model=Book.__name__,
                                                          product_id=obj.pk, print_type='ORI', stock__gt=0)

        return inventory_objects.exists()

    def get_color_available(self, obj):
        inventory_objects = Inventory.objects.filter(product_model=Book.__name__,
                                                     product_id=obj.pk, print_type='COL', stock__gt=0)

        return inventory_objects.exists()

    def get_economy_available(self, obj):
        inventory_objects = Inventory.objects.filter(product_model=Book.__name__,
                                                     product_id=obj.pk, print_type='ECO', stock__gt=0)

        return inventory_objects.exists()

    def get_used_copy_available(self, obj):
        inventory_objects = Inventory.objects.filter(product_model=Book.__name__,
                                                     product_id=obj.pk, is_new=0, stock__gt=0)

        return inventory_objects.exists()

    def get_market_price(self, obj):
        price_matrix_objects = PriceMatrix.objects.filter(product_model=Book.__name__,
                                                          product_code=obj.code, is_new=1, print_type='ECO')\
            .values('market_price')
        return price_matrix_objects.first()['market_price'] if price_matrix_objects.exists() else None

    def get_base_price(self, obj):
        price_matrix_objects = PriceMatrix.objects.filter(product_model=Book.__name__,
                                                          product_code=obj.code, is_new=1, print_type='ECO') \
            .values('base_price')

        return price_matrix_objects.first()['base_price'] if price_matrix_objects.exists() else None

    class Meta:
        model = Book
        fields = ('id', 'code', 'title', 'title_2', 'subtitle', 'subtitle_2', 'description', 'description_2', 'show_2',
                  'sale_available', 'market_price', 'buy_options', 'rent_options', 'base_price', 'page_count', 'categories', 'publisher', 'authors', 'tags', 'images',
                  'language', 'rent_available', 'slug', 'original_available', 'color_available', 'date_created',
                  'economy_available', 'used_copy_available', 'last_updated')

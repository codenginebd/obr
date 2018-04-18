from book_rental.api.serializers.author_serializer import AuthorSerializer
from book_rental.api.serializers.book_language_serializer import BookLanguageSerializer
from book_rental.api.serializers.publisher_serializer import PublisherSerializer
from book_rental.models.sales.book import Book
from ecommerce.api.serializers.category_serializer import CategorySerializer
from ecommerce.api.serializers.product_image_serializer import ProductImageSerializer
from ecommerce.api.serializers.rent_plan_serializer import RentPlanSerializer
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
    price_currency = serializers.SerializerMethodField()
    original_available = serializers.SerializerMethodField()
    color_available = serializers.SerializerMethodField()
    economy_available = serializers.SerializerMethodField()
    used_copy_available = serializers.SerializerMethodField()
    buy_options = serializers.SerializerMethodField()
    rent_options_eco_new = serializers.SerializerMethodField()
    is_rent_available = serializers.SerializerMethodField()
    rent_options = serializers.SerializerMethodField()
    is_sale_available = serializers.SerializerMethodField()
    product_type = serializers.SerializerMethodField()

    def get_product_type(self, obj):
        return obj.__class__.__name__

    def get_rent_options(self, obj):
        options = {
            "New": [],
            "Used": []
        }
        price_matrix_objects = PriceMatrix.objects.filter(product_model=Book.__name__,
                                                          product_code=obj.code, is_new=1, is_rent=True)
        if price_matrix_objects.exists():
            price_matrix_object = price_matrix_objects.first()
            rent_plans = price_matrix_object.rent_plans.all()
            for rent_plan_object in rent_plans:
                options["New"] += [
                    {
                        "name": rent_plan_object.verbose_name(),
                        "days": rent_plan_object.days
                    }
                ]
        price_matrix_objects = PriceMatrix.objects.filter(product_model=Book.__name__,
                                                          product_code=obj.code, is_new=0, is_rent=True)
        if price_matrix_objects.exists():
            price_matrix_object = price_matrix_objects.first()
            rent_plans = price_matrix_object.rent_plans.all()
            for rent_plan_object in rent_plans:
                options["Used"] += [
                    {
                        "name": rent_plan_object.verbose_name(),
                        "days": rent_plan_object.days
                    }
                ]
        options["new_options_available"] = True if options["New"] else False
        options["used_options_available"] = True if options["Used"] else False
        return options


    def get_is_sale_available(self, obj):
        inventory_objects = Inventory.objects.filter(product_model=Book.__name__,
                                                     product_id=obj.pk, stock__gt=0, available_for_sale=True)
        return inventory_objects.exists()

    def get_is_rent_available(self, obj):
        inventory_objects = Inventory.objects.filter(product_model=Book.__name__,
                                                     product_id=obj.pk, stock__gt=0, available_for_rent=True)
        return inventory_objects.exists()

    def get_price_currency(self, obj):
        price_matrix_objects = PriceMatrix.objects.filter(product_model=Book.__name__,
                                                          product_code=obj.code)

        if price_matrix_objects.exists():
            return price_matrix_objects.first().currency.short_name
        return None

    def get_buy_options(self, obj):
        inventory_objects = Inventory.objects.filter(product_model=Book.__name__,
                                                     product_id=obj.pk, stock__gt=0, is_new=1)
        options = {
            "New": [],
            "Used": []
        }
        for inventory_object in inventory_objects:
            options["New"] += [
                {
                    "short_name": inventory_object.print_type,
                    "full_name": inventory_object.print_type_full_name
                }
            ]
        inventory_objects = Inventory.objects.filter(product_model=Book.__name__,
                                                     product_id=obj.pk, stock__gt=0, is_new=0)
        for inventory_object in inventory_objects:
            options["Used"] += [
                {
                    "short_name": inventory_object.print_type,
                    "full_name": inventory_object.print_type_full_name
                }
            ]
        options["new_available"] = True if options["New"] else False
        options["used_available"] = True if options["Used"] else False
        return options

    def get_rent_options_eco_new(self, obj):
        price_matrix_objects = PriceMatrix.objects.filter(product_model=Book.__name__,
                                                          product_code=obj.code, is_new=1, print_type='ECO',is_rent=True)
        if price_matrix_objects.exists():
            rp_objects = price_matrix_objects.first().rent_plans.all()
            rps = RentPlanSerializer(rp_objects, many=True)
            return rps.data
        return []

    def get_original_available(self, obj):
        inventory_objects = Inventory.objects.filter(product_model=Book.__name__,
                                                          product_id=obj.pk, is_new=1,print_type='ORI', stock__gt=0)

        return inventory_objects.exists()

    def get_color_available(self, obj):
        inventory_objects = Inventory.objects.filter(product_model=Book.__name__,
                                                     product_id=obj.pk, is_new=1,print_type='COL', stock__gt=0)

        return inventory_objects.exists()

    def get_economy_available(self, obj):
        inventory_objects = Inventory.objects.filter(product_model=Book.__name__,
                                                     product_id=obj.pk, is_new=1,print_type='ECO', stock__gt=0)

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
        fields = ('id', 'code', 'product_type', 'title', 'title_2', 'isbn', 'edition', 'publish_date', 'subtitle', 'subtitle_2', 'description', 'description_2', 'show_2',
                  'sale_available', 'market_price', 'price_currency', 'is_sale_available', 'is_rent_available', 'buy_options', 'rent_options', 'rent_options_eco_new',
                  'base_price', 'page_count', 'categories', 'publisher', 'authors', 'tags', 'images',
                  'language', 'rent_available', 'slug', 'original_available', 'color_available', 'date_created',
                  'economy_available', 'used_copy_available', 'last_updated')

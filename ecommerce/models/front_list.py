from django.db import models
from django.urls.base import reverse

from ecommerce.models.front_list_product import FrontListProduct
from ecommerce.models.front_palette import FrontPalette
from ecommerce.models.sales.category import ProductCategory
from generics.models.base_entity import BaseEntity


class FrontList(BaseEntity):
    title = models.CharField(max_length=400)
    title_2 = models.CharField(max_length=400, null=True)
    show_2 = models.BooleanField(default=False)
    description = models.TextField(null=True)
    by_rule = models.BooleanField(default=False)
    category = models.ForeignKey(ProductCategory, null=True)
    rule_name = models.CharField(max_length=100, null=True)  # FrontListRule.TOP_X_PTC_DISCOUNT.value
    top_limit = models.IntegerField(default=0)
    products = models.ManyToManyField(FrontListProduct)
    detail_url = models.CharField(max_length=200)
    palette = models.ForeignKey(FrontPalette)


    def get_product_list(self):
        return []

    def populate_products(self):
        pass

    @classmethod
    def show_create(cls):
        return True

    @classmethod
    def get_create_link(cls):
        return reverse("admin_front_list_create_view")

    @classmethod
    def get_table_headers(self):
        return ["ID", "Code", "Title", "Title 2", "Show 2", "By Rule", "Rule Name", "Details"]

    @classmethod
    def prepare_table_data(cls, queryset):
        data = []
        for q_object in queryset:
            data += [
                [q_object.pk, q_object.code, q_object.title, q_object.title_2,
                 "Yes" if q_object.show_2 else "No", "Yes" if q_object.by_rule else "No",
                 q_object.rule_name,
                 '<a href="%s">Details</a>' % q_object.get_detail_link(object_id=q_object.pk)]
            ]
        return data
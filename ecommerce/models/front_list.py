from django.db import models
from ecommerce.models.front_list_product import FrontListProduct
from generics.models.base_entity import BaseEntity


class FrontList(BaseEntity):
    title = models.CharField(max_length=400)
    title_2 = models.CharField(max_length=400, null=True)
    show_2 = models.BooleanField(default=False)
    description = models.TextField(null=True)
    by_rule = models.BooleanField(default=False)
    rule_name = models.CharField(max_length=100, null=True)  # FrontListRule.TOP_X_PTC_DISCOUNT.value
    products = models.ManyToManyField(FrontListProduct)


    def get_product_list(self):
        return []

    def populate_products(self):
        pass
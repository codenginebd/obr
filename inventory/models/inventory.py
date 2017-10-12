from django.db import models
from django.urls.base import reverse

from ecommerce.models.sales.warehouse import Warehouse
from generics.models.base_entity import BaseEntity


class Inventory(BaseEntity):
    product_id = models.BigIntegerField(default=0)
    product_model = models.CharField(max_length=200)
    warehouse = models.ForeignKey(Warehouse)
    stock = models.BigIntegerField(default=0)
    available_for_buy = models.BooleanField(default=False)
    available_for_rent = models.BooleanField(default=False)
    available_for_sale = models.BooleanField(default=False)
    is_new = models.IntegerField(default=0)
    print_type = models.CharField(max_length=50) # COL, ORI, ECO #Color, Original and Economy
    comment = models.TextField(null=True)

    @property
    def print_type_full_name(self):
        if self.print_type == 'ORI':
            return "Original"
        elif self.print_type == 'COL':
            return "Color"
        elif self.print_type == 'ECO':
            return "Economy"

    @classmethod
    def show_create(cls):
        return True

    @classmethod
    def show_edit(cls):
        return True

    @classmethod
    def get_create_link(cls):
        return reverse("admin_inventory_create_view")
from django.db import models

from ecommerce.models.sales.warehouse import Warehouse
from generics.models.base_entity import BaseEntity


class Inventory(BaseEntity):
    product_id = models.BigIntegerField(default=0)
    product_model = models.CharField(max_length=200)
    warehouse = models.ForeignKey(Warehouse)
    stock = models.BigIntegerField(default=0)
    available_for_rent = models.BooleanField(default=False)
    is_new = models.IntegerField(default=0)
    print_type = models.CharField(max_length=50) # COL, ORI, ECO #Color, Original and Economy
    comment = models.TextField(null=True)
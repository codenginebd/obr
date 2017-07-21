from django.db import models
from generics.models.base_entity import BaseEntity
from generics.models.sales.warehouse import Warehouse


class Inventory(BaseEntity):
    product_type = models.CharField(max_length=200)
    warehouse = models.ForeignKey(Warehouse)
    stock = models.BigIntegerField(default=0)
    is_new = models.IntegerField(default=0)
    available_for_rent = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
from django.db import models
from generics.models.base_entity import BaseEntity


class InventoryTransaction(BaseEntity):
    transaction_type = models.CharField(max_length=100) # STOCK_IN, STOCK_OUT, TNX_DB, TNX_CR
    qty = models.BigIntegerField(default=0)
    counter_part_id = models.BigIntegerField(default=0)
    counter_part_model = models.CharField(max_length=100)
    product_id = models.BigIntegerField(default=0)
    product_model = models.CharField(max_length=100)
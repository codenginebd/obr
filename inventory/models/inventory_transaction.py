from django.db import models

from ecommerce.models.sales.warehouse import Warehouse
from generics.models.base_entity import BaseEntity
from inventory.models.product_supplier import ProductSupplier


class InventoryTransaction(BaseEntity):
    transaction_type = models.CharField(max_length=100) # STOCK_IN, STOCK_OUT, TNX_DB, TNX_CR
    qty = models.BigIntegerField(default=0)
    counter_part_id = models.BigIntegerField(null=True)
    counter_part_model = models.CharField(max_length=100, blank=True, null=True)
    supplier = models.ForeignKey(ProductSupplier, null=True, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product_id = models.BigIntegerField(default=0)
    product_model = models.CharField(max_length=100)
    is_new = models.IntegerField(default=0)
    print_type = models.CharField(max_length=50)  # COL, ORI, ECO
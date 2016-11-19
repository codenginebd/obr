from django.db import models

from generics.models.base_entity import BaseEntity
from inventory.models.inventory import BookInventory
from inventory.models.warehouse import BookWarehouse


class WarehouseInventory(BaseEntity):
    warehouse = models.ForeignKey(BookWarehouse)
    inventory = models.ForeignKey(BookInventory)
    stock = models.BigIntegerField(default=0)
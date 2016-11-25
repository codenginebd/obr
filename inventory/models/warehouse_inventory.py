from django.db import models

from generics.models.base_entity import BaseEntity
from inventory.models.inventory import Inventory
from inventory.models.warehouse import BookWarehouse


class WarehouseInventory(Inventory):
    warehouse = models.ForeignKey(BookWarehouse)
    
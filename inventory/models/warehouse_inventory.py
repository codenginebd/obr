from django.db import models
from inventory.models.inventory import Inventory
from inventory.models.warehouse import BookWarehouse


class WarehouseInventory(Inventory):
    warehouse = models.ForeignKey(BookWarehouse)
    
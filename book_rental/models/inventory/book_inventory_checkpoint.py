from django.db import models

class BookInventoryCheckPoint(InventoryCheckPoint):
    book = models.ForeignKey(Book)
    inventory = models.ForeignKey(BookInventory)
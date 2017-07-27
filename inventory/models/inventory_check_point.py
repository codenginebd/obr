from django.db import models

class InventoryCheckPoint(BaseEntity):
     supplier = models.ForeignKey(Supplier)
     current_stock = models.BinIntegerField(default=0)
     is_new = models.BooleanField(default=True)
     available_for_rent = models.BooleanField(default=False)
     
     
     class Meta:
         abstract = True
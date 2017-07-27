from django.db import models

class InventoryTransaction(BaseEntity):
    transaction_type = models.CharField(max_length=100) # STOCK_IN, STOCK_OUT, TNX_DB, TNX_CR
    qty = models.BigIntegerField(default=0)
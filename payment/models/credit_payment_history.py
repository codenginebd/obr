from django.db import models
from generics.models.base_entity import BaseEntity

class CreditPayHistory(BaseEntity):
    credit_amount = models.DecimalField(max_digits=20, decimal_places=2)
    ref_id = models.BigIntegerField(default=0)
    ref_code = models.CharField(max_length=500, blank=True, null=True)
    transaction_type = models.CharField(max_length=500)
    transaction_description = models.TextField(default='')
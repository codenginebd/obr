from django.db import models
from generics.models.base_entity import BaseEntity

class WalletCreditBreakdown(BaseEntity):
    credit_amount = models.DecimalField(max_digits=20, decimal_places=2)
    expiry_time = models.IntegerField(default=0)
    expired = models.BooleanField(False)
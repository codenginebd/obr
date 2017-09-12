from django.db import models

from enums import TransactionTypes
from generics.models.base_entity import BaseEntity


class CreditPayHistory(BaseEntity):
    credit_amount = models.DecimalField(max_digits=20, decimal_places=2)
    ref_id = models.BigIntegerField(null=True)
    ref_code = models.CharField(max_length=500, blank=True, null=True)
    transaction_type = models.IntegerField(default=TransactionTypes.CREDIT_STORE.value)
    transaction_description = models.TextField(default='')
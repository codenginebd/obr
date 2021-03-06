from django.contrib.auth.models import User
from django.db import models
from enums import PaymentStatus
from generics.models.base_entity import BaseEntity

from payment.models.currency import Currency


class PaymentTransaction(BaseEntity):
    payment_method = models.IntegerField() # e.g PAYMENT_METHODS.STORE_CREDIT.value
    transaction_code = models.CharField(max_length=200)
    payment_detail_id = models.BigIntegerField(null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, related_name='payment_received_for', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.IntegerField(default=PaymentStatus.PENDING.value)
    payment_received_by = models.ForeignKey(User, null=True, related_name='payment_received_by', on_delete=models.CASCADE)
    description = models.TextField(null=True)
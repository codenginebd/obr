from django.contrib.auth.models import User
from django.db import models
from generics.models.base_entity import BaseEntity
from payment.models.payment_method import PaymentMethod


class PaymentTransaction(BaseEntity):
    payment_method = models.IntegerField() # e.g PAYMENT_METHODS.STORE_CREDIT.value
    transaction_code = models.CharField(max_length=200)
    payment_detail_id = models.BigIntegerField(null=True)
    currency = models.ForeignKey(Currency)
    user = models.ForeignKey(User, null=True, related_name='payment_received_for')
    total = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.IntegerField(default=PAYMENT_STATUS.PENDING.value)
    payment_received_by = models.ForeignKey(User, null=True, related_name='payment_received_by')
    description = models.TextField(null=True)
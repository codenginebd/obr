from django.contrib.auth.models import User
from django.db import models
from generics.models.base_entity import BaseEntity
from payment.models.payment_method import PaymentMethod


class PaymentTransaction(BaseEntity):
    payment_method = models.ForeignKey(PaymentMethod)
    user = models.ForeignKey(User, related_name='payment_received_for')
    total = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.IntegerField(default=0)
    payment_received_by = models.ForeignKey(User, null=True, related_name='payment_received_by')
from django.contrib.auth.models import User
from django.db import models
from generics.models.base_entity import BaseEntity
from inventory.models.warehouse import Warehouse
from bauth.models.address import Address
from payment.models.payment_transaction import PaymentTransaction
from promotion.models.promotion import Promotion


class Order(BaseEntity):
    user = models.ForeignKey(User, null=True)
    status = models.IntegerField(default=0) # placed, in progress, delivered
    addresses = models.ManyToManyField(Address)
    warehouse = models.ForeignKey(Warehouse, null=True)
    delivered_by = models.ForeignKey(User, related_name='order_delivered_by', null=True)
    payment_status = models.IntegerField(default=0) # Not Processed, Processed and Successful, Processed and Failed
    payment = models.ForeignKey(PaymentTransaction, null=True)
    coupon_applied = models.BooleanField(default=False)
    coupon_code = models.CharField(max_length=200, blank=True, null=True)
    promotion_applied = models.BooleanField(default=False)
    promotion = models.ForeignKey(Promotion, null=True)

    class Meta:
        abstract = True
from django.contrib.auth.models import User
from django.db import models
from generics.models.base_entity import BaseEntity
from inventory.models.warehouse import BookWarehouse
from order.models.order_breakdown import BookOrderBreakdown
from bauth.models.address import Address
from payment.models.payment_transaction import PaymentTransaction


class BookOrder(BaseEntity):
    user = models.ForeignKey(User)
    breakdown = models.ManyToManyField(BookOrderBreakdown)
    status = models.IntegerField(default=0) # placed, in progress, delivered
    addresses = models.ManyToManyField(Address)
    warehouse = models.ForeignKey(BookWarehouse)
    delivered_by = models.ForeignKey(User, related_name='order_delivered_by', null=True)
    payment_status = models.IntegerField(default=0) # Not Processed, Processed and Successful, Processed and Failed
    payment = models.ForeignKey(PaymentTransaction, null=True)
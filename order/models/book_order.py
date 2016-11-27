from django.db import models
from generics.models.base_entity import BaseEntity
from order.models.order_breakdown import BookOrderBreakdown


class BookOrder(BaseEntity):
    user = models.ForeignKey(User)
    breakdown = models.ManyToMany(BookOrderBreakdown)
    status = models.IntegerField(default=0) # placed, in progress, delivered
    addresses = models.ManyToManyField(Address)
    warehouse = models.ForeignKey(BookWarehouse)
    delivered_by = models.ForeignKey(User, related_name='order_delivered_by')
    payment_status = models.IntegerField(default=0) # Not Processed, Processed and Successful, Processed and Failed
    payment = models.ForeignKey(PaymentTransaction, null=True)
    payment_received_by = models.ForeignKey(User, related_name='payment_received_by')
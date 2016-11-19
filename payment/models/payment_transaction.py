from django.db import models

from clients.models.client_user import ClientUser
from clients.models.delivery_agent import DeliveryAgent
from generics.models.base_entity import BaseEntity
from order.models.book_order import BookOrder
from payment.models.payment_method import PaymentMethod


class PaymentTransaction(BaseEntity):
    payment_method = models.ForeignKey(PaymentMethod)
    user = models.ForeignKey(ClientUser)
    order = models.ForeignKey(BookOrder)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.IntegerField(default=0)
    delivery_agent = models.ForeignKey(DeliveryAgent, null=True)
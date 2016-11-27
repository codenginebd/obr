from django.contrib.auth.models import User
from django.db import models
from clients.models.client_user import ClientUser
from generics.models.base_entity import BaseEntity
from order.models.book_order import BookOrder
from payment.models.payment_method import PaymentMethod


class PaymentTransaction(BaseEntity):
    payment_method = models.ForeignKey(PaymentMethod)
    user = models.ForeignKey(ClientUser)
    order = models.ForeignKey(BookOrder)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.IntegerField(default=0)
    payment_received_by = models.ForeignKey(User, null=True)
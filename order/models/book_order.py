from django.db import models
from book_rental.models.base_entity import BaseEntity
from clients.models.client_user import ClientUser
from order.models.order_breakdown import BookOrderBreakdown


class BookOrder(BaseEntity):
    user = models.ForeignKey(ClientUser)
    breakdown = models.ManyToMany(BookOrderBreakdown)
    status = models.IntegerField(default=0)
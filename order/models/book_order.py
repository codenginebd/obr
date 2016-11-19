from django.db import models

from clients.models.client_user import ClientUser
from generics.models.base_entity import BaseEntity
from order.models.order_breakdown import BookOrderBreakdown


class BookOrder(BaseEntity):
    user = models.ForeignKey(ClientUser)
    breakdown = models.ManyToMany(BookOrderBreakdown)
    status = models.IntegerField(default=0)
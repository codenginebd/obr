from django.db import models
from bauth.models.address import Adress
from generics.models.base_entity import BaseEntity


class BookWarehouse(BaseEntity):
    name = models.CharField(max_length=500)
    address = models.ForeignKey(Adress)
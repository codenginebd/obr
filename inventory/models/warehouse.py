from django.db import models
from bauth.models.address import Address
from generics.models.base_entity import BaseEntity


class Warehouse(BaseEntity):
    name = models.CharField(max_length=500)
    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
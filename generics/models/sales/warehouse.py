from django.db import models

from bauth.models.phone import Phone
from generics.models.base_entity import BaseEntity


class Warehouse(BaseEntity):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    contact = models.ForeignKey(Phone, null=True)
    warehouse_manager = models.CharField(max_length=200, blank=True, null=True)
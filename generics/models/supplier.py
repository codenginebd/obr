from django.db import models
from generics.models.base_entity import BaseEntity


class ProductSupplier(BaseEntity):
    name = models.CharField(max_length=200)
    address_line1 = models.CharField(max_length=500, null=True, blank=True)
    address_line2 = models.CharField(max_length=500, null=True, blank=True)
    address_line3 = models.CharField(max_length=500, null=True, blank=True)
    address_line4 = models.CharField(max_length=500, null=True, blank=True)
    phone_number1 = models.CharField(max_length=20, null=True, blank=True)
    phone_number2 = models.CharField(max_length=20, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

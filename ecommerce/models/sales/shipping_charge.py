from django.db import models
from generics.models.base_entity import BaseEntity

"""
shipping_condition = 1 for by amount, 2 for by area
"""


class ShippingCharge(BaseEntity):
    shipping_condition = models.BooleanField(default=False)
    shipping_condition_amount = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)
    shipping_state = models.CharField(max_length=6, blank=True)
    excluded_zip_codes = models.CharField(max_length=1536, blank=True)
    shipping_cost = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)
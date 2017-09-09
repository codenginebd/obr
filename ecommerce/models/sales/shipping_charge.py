from django.db import models
from django.db.models.query_utils import Q
from bauth.models.zip_code import ZipCode
from generics.models.base_entity import BaseEntity

"""
shipping_condition = 1 for by amount, 2 for by area
"""


class ShippingCharge(BaseEntity):
    shipping_condition = models.BooleanField(default=False)
    shipping_condition_amount = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)
    shipping_state = models.CharField(max_length=6, blank=True)  # Zilla
    excluded_zip_codes = models.ManyToManyField(ZipCode, related_name='excluded_zip_codes')
    special = models.BooleanField(default=False)
    special_zip_codes = models.ManyToManyField(ZipCode, related_name='special_zip_codes')
    shipping_cost = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)

    @classmethod
    def get_shipping_charge(cls, shipping_state, total_amount, zip_code=None):
        shipping_charge_objects = cls.objects.all()

        shipping_charge_objects = shipping_charge_objects.filter(Q(shipping_state__isnull=True) |
                                                                 (Q(shipping_state__isnull=False) &
                                                                  Q(shipping_state=shipping_state)))

        shipping_charge_objects = shipping_charge_objects.filter(Q(shipping_condition=False) |
                                                                     (Q(shipping_condition=True) &
                                                                      Q(shipping_condition_amount__lte=total_amount)))

        if zip_code:
            shipping_charge_objects = shipping_charge_objects.filter(special=True,
                                                                     special_zip_codes__zip_code__in=[zip_code])

        if shipping_charge_objects.exists():
            shipping_charge_object = shipping_charge_objects.first()
            return shipping_charge_object.shipping_cost
        return None
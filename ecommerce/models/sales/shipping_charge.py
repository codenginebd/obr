from django.db import models, transaction
from django.db.models.query_utils import Q
from bauth.models.zip_code import ZipCode
from generics.models.base_entity import BaseEntity

"""
shipping_condition = 1 for by amount, 2 for by area
"""


class ShippingCharge(BaseEntity):
    shipping_condition = models.BooleanField(default=False)
    shipping_condition_amount = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)
    shipping_state = models.CharField(max_length=100, blank=True, null=True)  # Zilla
    excluded_zip_codes = models.ManyToManyField(ZipCode, related_name='excluded_zip_codes')
    special = models.BooleanField(default=False)
    special_zip_codes = models.ManyToManyField(ZipCode, related_name='special_zip_codes')
    shipping_cost = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)

    @classmethod
    def create_or_update_shipping_charge(cls, shipping_cost, pk=None, shipping_state = None, shipping_condition=False,
                                         shipping_condition_amount=None, excluded_zip_codes=[],
                                         special=False, special_zip_codes=[]):
        with transaction.atomic():
            try:
                if pk:
                    shipping_charge_objects = cls.objects.filter(pk=pk)
                    if shipping_charge_objects.exists():
                        shipping_charge_object = shipping_charge_objects.first()
                    else:
                        return False
                else:
                    shipping_charge_object = cls()

                shipping_charge_object.shipping_cost = shipping_cost

                if shipping_state:
                    shipping_charge_object.shipping_state = shipping_state

                shipping_charge_object.shipping_condition = shipping_condition

                if shipping_condition:
                    if shipping_condition_amount:
                        shipping_charge_object.shipping_condition_amount = shipping_condition_amount
                    else:
                        return False

                shipping_charge_object.special = special

                shipping_charge_object.save()

                if special:
                    if not special_zip_codes:
                        return False
                    for zcode in special_zip_codes:
                        zipcode_objects = ZipCode.objects.filter(zip_code=zcode)
                        if zipcode_objects.exists():
                            zipcode = zipcode_objects.first()
                        else:
                            zipcode = ZipCode(zip_code=zcode)
                            zipcode.save()
                        zip_codes = [zipcode]
                        shipping_charge_object.special_zip_codes.add(*zip_codes)
                else:
                    for zcode in excluded_zip_codes:
                        zipcode_objects = ZipCode.objects.filter(zip_code=zcode)
                        if zipcode_objects.exists():
                            zipcode = zipcode_objects.first()
                        else:
                            zipcode = ZipCode(zip_code=zcode)
                            zipcode.save()
                        zip_codes = [zipcode]
                        shipping_charge_object.excluded_zip_codes.add(*zip_codes)

                return True
            except Exception as exp:
                return False

    @classmethod
    def get_shipping_charge(cls, shipping_state, total_amount, zip_code=None):
        shipping_charge_objects = cls.objects.all()

        shipping_charge_objects = shipping_charge_objects.filter(Q(shipping_state__isnull=True) |
                                                                 (Q(shipping_state__isnull=False) &
                                                                  Q(shipping_state=shipping_state)))

        shipping_charge_objects = shipping_charge_objects.filter(Q(shipping_condition=False) |
                                                                     (Q(shipping_condition=True) &
                                                                      Q(shipping_condition_amount__lte=total_amount)))
        no_special_found = False
        if zip_code:
            special_shipping_charges = shipping_charge_objects.filter(special=True,
                                                                     special_zip_codes__zip_code__in=[zip_code])

            if special_shipping_charges.exists():
                shipping_charge_objects = special_shipping_charges
            else:
                no_special_found = True

        if no_special_found:
            shipping_charge_objects = shipping_charge_objects.exclude(special=True)

        shipping_charge_objects = shipping_charge_objects.order_by('shipping_cost')
        if shipping_charge_objects.exists():
            shipping_charge_object = shipping_charge_objects.first()
            return shipping_charge_object.shipping_cost
        return None
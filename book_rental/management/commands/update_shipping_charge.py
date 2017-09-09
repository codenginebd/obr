from django.core.management.base import BaseCommand

from bauth.models.zip_code import ZipCode
from ecommerce.models.sales.shipping_charge import ShippingCharge


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Starting...!")

        shipping_charge = ShippingCharge()
        shipping_charge.shipping_condition = False
        shipping_charge.shipping_state = 'Dhaka'
        shipping_charge.shipping_cost = 30
        shipping_charge.save()

        zip_codes = [ ZipCode(zip_code='1230').save() ]
        shipping_charge.excluded_zip_codes.add(*zip_codes)

        shipping_charge = ShippingCharge()
        shipping_charge.shipping_condition = False
        shipping_charge.shipping_state = 'Dhaka'
        shipping_charge.shipping_cost = 10
        shipping_charge.special = True
        shipping_charge.save()

        zip_codes = [ZipCode(zip_code='1230').save()]
        shipping_charge.special_zip_codes.add(*zip_codes)

        shipping_charge = ShippingCharge()
        shipping_charge.shipping_condition = False
        shipping_charge.shipping_state = 'Chittagong'
        shipping_charge.shipping_cost = 60
        shipping_charge.save()

        shipping_charge = ShippingCharge()
        shipping_charge.shipping_condition = False
        shipping_charge.shipping_state = 'Chittagong'
        shipping_charge.shipping_cost = 30
        shipping_charge.special = True
        shipping_charge.save()
        zip_codes = [ZipCode(zip_code='1400').save()]
        shipping_charge.special_zip_codes.add(*zip_codes)

        shipping_charge = ShippingCharge()
        shipping_charge.shipping_condition = False
        shipping_charge.shipping_state = 'Sylhet'
        shipping_charge.shipping_cost = 50
        shipping_charge.save()

        shipping_charge = ShippingCharge()
        shipping_charge.shipping_condition = True
        shipping_charge.shipping_condition_amount = 500
        shipping_charge.shipping_state = 'Dhaka'
        shipping_charge.shipping_cost = 20
        shipping_charge.save()

        print("Ended.")
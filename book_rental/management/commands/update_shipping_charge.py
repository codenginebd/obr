from django.core.management.base import BaseCommand

from bauth.models.zip_code import ZipCode
from ecommerce.models.sales.shipping_charge import ShippingCharge


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Cleaning all objects')
        ShippingCharge.objects.all().delete()

        print("Starting...!")

        charge = ShippingCharge.create_or_update_shipping_charge(shipping_cost=300)
        print(charge)

        charge = ShippingCharge.create_or_update_shipping_charge(shipping_cost=30, shipping_state='Dhaka', excluded_zip_codes=['1230'])
        print(charge)

        charge = ShippingCharge.create_or_update_shipping_charge(shipping_cost=10, shipping_state='Dhaka', special=True,
                                                                 special_zip_codes=['1230'])
        print(charge)

        charge = ShippingCharge.create_or_update_shipping_charge(shipping_cost=20, shipping_state='Dhaka',
                                                                 shipping_condition=True, shipping_condition_amount=500)

        print(charge)

        charge = ShippingCharge.create_or_update_shipping_charge(shipping_cost=60, shipping_state='Chittagong')

        print(charge)

        charge = ShippingCharge.create_or_update_shipping_charge(shipping_cost=30, shipping_state='Chittagong',
                                                                 special=True, special_zip_codes=['1400'])

        print(charge)

        charge = ShippingCharge.create_or_update_shipping_charge(shipping_cost=50, shipping_state='Sylhet')

        print(charge)

        print("Ended.")

        print("Total: %s" % ShippingCharge.objects.all().count())
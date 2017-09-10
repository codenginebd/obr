from book_rental.models.sales.book import Book
from ecommerce.models.sales.shipping_charge import *
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        charge = ShippingCharge.get_shipping_charge('Dhaka', 500, '1230')
        print(charge)
        charge = ShippingCharge.get_shipping_charge('Chittagong', 500, '1230')
        print(charge)
        charge = ShippingCharge.get_shipping_charge('Chittagong', 500, '1400')
        print(charge)
        charge = ShippingCharge.get_shipping_charge('Barishal', 500, '1230')
        print(charge)

        b = Book.objects.filter(pk=1).first().code
        print(b)
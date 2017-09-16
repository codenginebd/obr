from book_rental.models.sales.book import Book
from ecommerce.models.sales.shipping_charge import *
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        # charge = ShippingCharge.get_shipping_charge('Dhaka', 500, '1230')
        # print(charge)
        # charge = ShippingCharge.get_shipping_charge('Chittagong', 500, '1230')
        # print(charge)
        # charge = ShippingCharge.get_shipping_charge('Chittagong', 500, '1400')
        # print(charge)
        # charge = ShippingCharge.get_shipping_charge('Barishal', 500, '1230')
        # print(charge)
        #
        # b = Book.objects.filter(pk=1).first().code
        # print(b)

        def check_list_exist(iter1, iter2):  # Checks if iter1 reside in iter2. iter2 is a 2d tuple
            print(iter1,iter2)
            for subiter in iter2:
                if len(iter1) != len(subiter):
                    return False
                all_matched = True
                for index, a in enumerate(iter1):
                    if a != subiter[index]:
                        all_matched = False
                if all_matched:
                    return True
            return False

        def get_matched_subtotal(iter1, iter2, max_index):
            if not max_index:
                return None
            for item in iter2:
                all_matched = []
                for i, a in enumerate(item):
                    if i > max_index:
                        break
                    all_matched += [item[i] == iter1[i]]
                if all(all_matched):
                    return item

        a1 = (1,'Book', True, 'ECO')
        a2 = ((2,'Book', False, 'ORI'), (1,'Book', True, 'ORI'))
        print(check_list_exist(a1,a2))
        a1 = [1, 'Book', True, 'ECO']
        a2 = [[2, 'Book', False, 'ORI'], [1, 'Book', True, 'ECO']]
        print(check_list_exist(a1, a2))
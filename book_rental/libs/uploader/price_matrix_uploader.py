import os
from django.conf import settings
from django.db import transaction
from datetime import datetime
from generics.models.sales.price_matrix import PriceMatrix
from generics.libs.utils import get_relative_path_to_media
from logger.models.error_log import ErrorLog


class PriceMatrixUploader(object):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs
        
    def handle_sale_price_upload(self):
        for row in self.data:
            with transaction.atomic():
                index = 0
                product_code = row[index]
                index += 1
                is_new = row[index]
                index += 1
                print_type = row[index]
                index += 1
                market_price = row[index]
                index += 1
                base_price = row[index]
                index += 1
                is_special_sale = row[index]
                index += 1
                special_sale_rate = row[index]
                index += 1
                offer_start_date = row[index]
                index += 1
                offer_end_date = row[index]
                index += 1
                currency = row[index]
                
                if any( [ not item for item in [ product_code, is_new, print_type, market_price, base_price, is_special_sale, currency ] ] ):
                    error_log = ErrorLog()
                    error_log.url = ''
                    error_log.stacktrace = 'Missing data.'
                    error_log.save()
                    continue
                    
                if not print_type in settings.SUPPORTED_PRINTING_TYPES:
                    pass
                
                price_objects = PriceMatrix.objects.filter(product_model='Book', product_code=product_code, is_new=is_new, print_type=print_type)
                
        
    def handle_rent_price_upload(self):
        for row in self.data:
            with transaction.atomic():
                index = 0
                rent_code = row[index]
                index += 1
                product_code = row[index]
                index += 1
                is_new = row[index]
                index += 1
                print_type = row[index]
                index += 1
                price_in_percentage = row[index]
                index += 1
                is_special_rent = row[index]
                index += 1
                special_rent_rate = row[index]
                index += 1
                offer_start_date = row[index]
                index += 1
                offer_end_date = row[index]
                index += 1
                currency = row[index]

    def handle_upload(self):
        self.data = self.data[1:]
        if self.kwargs.get('price_type', 'sale') == 'rent': #'sale' or 'rent'
            self.handle_rent_price_upload()
        else:
            self.handle_sale_price_upload()
        # product_code	is new	print type	market price	base price	is special sale offer	special offer rate	offer start date	offer end date	currency
        # rent_code	product_code	is new	print type	price in percentage	special rent offer  special rent rate	offer start date	offer end date currency
                
                
                
                
                
from decimal import Decimal
from django.conf import settings
from django.db import transaction
from engine.clock.Clock import Clock
from generics.models.sales.currency import Currency
from generics.models.sales.price_matrix import PriceMatrix
from generics.models.sales.product import Product
from generics.models.sales.rent_plan import RentPlan
from generics.models.sales.rent_plan_relation import RentPlanRelation
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
                    
                product_objects = Product.objects.filter(code=product_code)
                if product_objects.exists():
                    product_object = product_objects.first()
                else:
                    ErrorLog.log(url='', stacktrace='Invalid product code supplied. Skipping... Data %s' % product_code)
                    continue
                    
                try:
                    is_new = int(is_new)
                    if is_new != 1 and is_new != 0:
                        ErrorLog.log(url='', stacktrace='Invalid is_new supplied. 1 or 0 expected. Skipping... Data %s' % row)
                        continue
                    if is_new == 1:
                        is_new = True
                    else:
                        is_new = False
                except:
                    ErrorLog.log(url='', stacktrace='Invalid is_new supplied. 1 or 0 expected. Skipping... Data %s' % row)
                    continue
                    
                if not print_type in settings.SUPPORTED_PRINTING_TYPES:
                    ErrorLog.log(url='', stacktrace='printing type must be in %s. Skipping...' % settings.SUPPORTED_PRINTING_TYPES)
                    continue
                    
                try:
                    market_price = Decimal(market_price)
                except:
                    ErrorLog.log(url='', stacktrace='Invalid market_price value. Decimal expected. Given: %s' % row)
                    continue
                    
                try:
                    base_price = Decimal(base_price)
                except:
                    ErrorLog.log(url='', stacktrace='Invalid base_price value. Decimal expected. Given: %s' % row)
                    continue
                    
                try:
                    is_special_sale = int(is_special_sale)
                    if is_special_sale != 1 and is_special_sale != 0:
                        ErrorLog.log(url='', stacktrace='Invalid is_special_sale supplied. 1 or 0 expected. Skipping... Data %s' % row)
                        continue
                    if is_special_sale == 1:
                        is_special_sale = True
                    else:
                        is_special_sale = False
                except:
                    ErrorLog.log(url='', stacktrace='Invalid is_special_sale supplied. 1 or 0 expected. Skipping... Data %s' % row)
                    continue
                    
                try:
                    special_sale_rate = Decimal(special_sale_rate)
                except:
                    ErrorLog.log(url='', stacktrace='Invalid special_sale_rate value. Decimal expected. Given: %s' % row)
                    continue
                    
                try:
                    offer_start_date = offer_start_date.date()
                except:
                    ErrorLog.log(url='', stacktrace='Invalid offer_start_date value. Skipping... Expected format: dd/mm/yyyy. Given' % row)
                    continue
                    
                try:
                    offer_end_date = offer_end_date.date()
                except:
                    ErrorLog.log(url='', stacktrace='Invalid offer_end_date value. Skipping... Expected format: dd/mm/yyyy. Given' % row)
                    continue
                    
                currency_objects = Currency.objects.filter(short_name=currency)
                if currency_objects.exists():
                    currency_object = currency_objects.first()
                else:
                    ErrorLog.log(url='', stacktrace='Invalid currency code value. Skipping...Data: ' % row)
                    continue
                    
                price_objects = PriceMatrix.objects.filter(product_model='Book', product_code=product_code, is_new=is_new, print_type=print_type)
                
                if price_objects.exists():
                    price_object = price_objects.first()
                else:
                    price_object = PriceMatrix(product_model='Book', product_code=product_code, is_new=is_new, print_type=print_type)
                    
                price_object.is_rent = False
                price_object.market_price = market_price
                price_object.base_price = base_price
                price_object.currency_id = currency_object.pk
                price_object.offer_date_start = Clock.convert_datetime_to_timestamp(offer_start_date)
                price_object.offer_date_end = Clock.convert_datetime_to_timestamp(offer_end_date)
                price_object.special_price = is_special_sale
                if is_special_sale:
                    price_object.offer_price_p = special_sale_rate / 100
                    price_object.offer_price_v = base_price * price_object.offer_price_p
                else:
                    price_object.offer_price_p = 1.0
                    price_object.offer_price_v = base_price
                    
                price_object.save()
                
                #Price Saved.

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
                
                if any( [ not item for item in [ rent_code, product_code, is_new, print_type, price_in_percentage, is_special_rent, currency ] ] ):
                    error_log = ErrorLog()
                    error_log.url = ''
                    error_log.stacktrace = 'Missing data.'
                    error_log.save()
                    continue
                    
                product_objects = Product.objects.filter(code=product_code)
                if product_objects.exists():
                    product_object = product_objects.first()
                else:
                    ErrorLog.log(url='', stacktrace='Invalid product code supplied. Skipping... Data %s' % product_code)
                    continue
                    
                try:
                    is_new = int(is_new)
                    if is_new != 1 and is_new != 0:
                        ErrorLog.log(url='', stacktrace='Invalid is_new supplied. 1 or 0 expected. Skipping... Data %s' % row)
                        continue
                    if is_new == 1:
                        is_new = True
                    else:
                        is_new = False
                except:
                    ErrorLog.log(url='', stacktrace='Invalid is_new supplied. 1 or 0 expected. Skipping... Data %s' % row)
                    continue
                    
                if not print_type in settings.SUPPORTED_PRINTING_TYPES:
                    ErrorLog.log(url='', stacktrace='printing type must be in %s. Skipping...' % settings.SUPPORTED_PRINTING_TYPES)
                    continue
                    
                try:
                    price_in_percentage = Decimal(price_in_percentage)
                except:
                    ErrorLog.log(url='', stacktrace='Invalid price_in_percentage value. Decimal expected. Given: %s' % row)
                    continue
                    
                try:
                    is_special_rent = int(is_special_rent)
                    if is_special_rent != 1 and is_special_rent != 0:
                        ErrorLog.log(url='', stacktrace='Invalid is_special_rent supplied. 1 or 0 expected. Skipping... Data %s' % row)
                        continue
                    if is_special_rent == 1:
                        is_special_rent = True
                    else:
                        is_special_rent = False
                except:
                    ErrorLog.log(url='', stacktrace='Invalid is_special_rent supplied. 1 or 0 expected. Skipping... Data %s' % row)
                    continue
                    
                try:
                    special_rent_rate = Decimal(special_rent_rate)
                except:
                    ErrorLog.log(url='', stacktrace='Invalid special_rent_rate value. Decimal expected. Given: %s' % row)
                    continue
                    
                try:
                    offer_start_date = offer_start_date.date()
                except:
                    ErrorLog.log(url='', stacktrace='Invalid offer_start_date value. Skipping... Expected format: dd/mm/yyyy. Given' % row)
                    continue
                    
                try:
                    offer_end_date = offer_end_date.date()
                except:
                    ErrorLog.log(url='', stacktrace='Invalid offer_end_date value. Skipping... Expected format: dd/mm/yyyy. Given' % row)
                    continue
                    
                currency_objects = Currency.objects.filter(short_name=currency)
                if currency_objects.exists():
                    currency_object = currency_objects.first()
                else:
                    ErrorLog.log(url='', stacktrace='Invalid currency code value. Skipping...Data: ' % row)
                    continue
                    
                price_objects = PriceMatrix.objects.filter(product_model='Book', product_code=product_code, is_new=is_new, print_type=print_type)
                
                if price_objects.exists():
                    price_object = price_objects.first()
                else:
                    ErrorLog.log(url='', stacktrace='No price matrix object exists for this. Skipping...Data: ' % row)
                    continue
                    
                rent_plan_objects = RentPlan.objects.filter(code=rent_code)
                if rent_plan_objects.exists():
                    rent_plan_object = rent_plan_objects.first()
                else:
                    ErrorLog.log(url='', stacktrace='No rent plan exists. Skipping...Data: ' % row)
                    continue
                    
                rent_rel_objects = RentPlanRelation.objects.filter(plan_id=rent_plan_object.pk, price_matrix_id=price_object.pk)
                if rent_rel_objects.exists():
                    rent_rel_object = rent_rel_objects.first()
                else:
                    rent_rel_object = RentPlanRelation(plan_id=rent_plan_object.pk, price_matrix_id=price_object.pk)
                    
                rent_rel_object.start_time = Clock.toUTCTimeStamp(offer_start_date)
                rent_rel_object.end_time = Clock.toUTCTimeStamp(offer_end_date)
                
                rent_rel_object.is_special_offer  = is_special_rent
                rent_rel_object.special_rate  = float(special_rent_rate)/100
                
                rent_rel_object.save()
                
                # Done. Continue to next.
                    

    def handle_upload(self):
        self.data = self.data[1:]
        if self.kwargs.get('price_type', 'sale') == 'rent': #'sale' or 'rent'
            self.handle_rent_price_upload()
        else:
            self.handle_sale_price_upload()
        # product_code	is new	print type	market price	base price	is special sale offer	special offer rate	offer start date	offer end date	currency
        # rent_code	product_code	is new	print type	price in percentage	special rent offer  special rent rate	offer start date	offer end date currency
                
                
                
                
                
from datetime import datetime
from django.conf import settings
from book_rental.models.sales.book import Book
from promotion.promotion_manager import PromotionManager
from inventory.models.inventory import Inventory

"""
Cart Structure

{
    'last_modified': datetime,
    'items': 
    {
        1213: 
        {
            'buy': 
            {
                    'qty': 10,
                    'unit_price': 100,
                    'subtotal': 1000,
                    'promo_applied': True,
                    'promo_code': 'ZacdaSds',
                    'discount_applied': True,
                    'discount_code': 'DSdsDcD',
                    'total': 500,
                    'currency_code': 'BDT'
            },
            'rent': 
            [
                {
                    'qty': 10,
                    'unit_price': 100,
                    'subtotal': 1000,
                    'rent_days': 30,
                    'promo_applied': True,
                    'promo_code': 'ZacdaSds',
                    'discount_applied': True,
                    'discount_code': 'DSdsDcD',
                    'total': 500,
                    'currency_code': 'BDT'
                }
            ],
            'sale': 
            {
                    'qty': 10,
                    'unit_price': 100,
                    'subtotal': 1000,
                    'total': 500,
                    'currency_code': 'BDT'
            }
        } 
    }
}

"""
    

class Cart(object):
    last_updated = datetime.utcnow()
    items = {}
    
    def __init__(self, request, *args, **kwargs):
        if not settings.CART_SESSION_ID in request.session:
            request.session[settings.CART_SESSION_ID] = {}
        self.cart = request.session[settings.CART_SESSION_ID]
        self.request = request
        
    def get_buy_items(self):
        return None
        
    def get_rent_items(self):
        return None
        
    def get_sale_items(self):
        return None
        
    def check_inventory(self, product_id, product_type, is_new, print_type, warehouse_id=None, check_rent_available=False):
        inventory_objects = Inventory.objects.filter(product_id=product_id, product_model=product_type, is_new=is_new, print_type=print_type, stock__gt=0)
        if warehouse_id:
            inventory_objects = inventory_objects.filter(warehouse_id=warehouse_id)
        if check_rent_available:
            inventory_objects = inventory_objects.filter(available_for_rent=True)
        return inventory_objects.exists()
        
    def add_to_cart(self, buy_type, product_code, product_type, is_new, print_type, qty, currency_code, warehouse_id=None, rent_days=None):
        product_objects = Book.objects.filter(code=product_code)
        if product_objects.exists():
            product_object = product_objects.first()
            
            # Now check step by step whether to proceed or not
            
            check_rent_price = True if buy_type == 'rent' else False
            
            inventory_exists = self.check_inventory(product_id=product_object.pk, product_type=product_type, is_new=is_new, print_type=print_type, warehouse_id=warehouse_id, check_rent_available=check_rent_price)
            
            if not inventory_exists:
                return False
               
            buy_effective_price = None
            rent_effective_price = None
            sale_effective_price = None
            if buy_type == 'buy':
                buy_effective_price = product_object.get_effective_base_price(is_new=is_new, print_type=print_type)
                if not buy_effective_price:
                    return False
            elif buy_type == 'rent':
                if not rent_days:
                    return False
                rent_effective_price = product_object.get_effective_rent_price_for_days(is_new=is_new, print_type=print_type, rent_days=rent_days)
                if not rent_effective_price:
                    return False                    
            elif buy_type == 'sale':
                sale_effective_price = product_object.get_sale_price(is_new=is_new, print_type=print_type)
                if not sale_effective_price:
                    return False        
            
            if not 'items' in self.cart.items():
                self.cart['items'] = {}
                
            if not product_object.pk in self.cart['items'].items():
                self.cart['items'][product_object.pk] = { 'buy': {  }, 'rent': [ ], 'sale': { } }
                
            if buy_type == 'buy':
                product_buy_cart = self.cart['items'][product_object.pk]['buy']
                
                if not 'qty' in product_buy_cart.items():
                    product_buy_cart['qty'] = qty
                else:
                    product_buy_cart['qty'] += qty
                
                product_buy_cart['unit_price'] = buy_effective_price
                
                subtotal = qty * buy_effective_price
                
                product_buy_cart['subtotal'] = subtotal
                
                promotion_manager_instance = PromotionManager()
                promo_applied, promo_code = promotion_manager_instance.apply_promotion(self)
                
                if promo_applied:
                    product_buy_cart['promo_applied'] = True
                    product_buy_cart['promo_code'] = promo_code
                else:
                    product_buy_cart['promo_applied'] = False
                    product_buy_cart['promo_code'] = None
                    
                product_buy_cart['currency_code'] = currency_code
                
                self.cart['items'][product_object.pk]['buy'] = product_buy_cart
            elif buy_type == 'rent':
                product_rent_cart = self.cart['items'][product_object.pk]['rent']
                
                self.cart['items'][product_object.pk]['rent'] = product_rent_cart
            elif buy_type == 'sale':
                product_sale_cart = self.cart['items'][product_object.pk]['sale']
                
                self.cart['items'][product_object.pk]['sale'] = product_sale_cart
            
    def save(self):
        self.cart['last_modified'] = datetime.utcnow()
        self.request.session[settings.CART_SESSION_ID] = self.cart
            
            
        
        
        
        
        
        
        
from datetime import datetime
from django.conf import settings
from book_rental.models.sales.book import Book

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
        
    def add_to_cart(self, buy_type, product_code, is_new, print_type, qty, unit_price, promo_applied, promo_code, discount_applied, discount_code, currency_code):
        product_objects = Book.objects.filter(code=product_code)
        if product_objects.exists():
            product_object = product_objects.first()
            if not 'items' in self.cart.items():
                self.cart['items'] = {}
                
            if not product_object.pk in self.cart['items'].items():
                self.cart['items'][product_object.pk] = { 'buy': {  }, 'rent': [ ], 'sale': { } }
                
            if buy_type == 'buy':
                product_buy_cart = self.cart['items'][product_object.pk]['buy']
                
                product_buy_cart['qty'] = qty
                
                base_price = product_object.get_effective_base_price(is_new=is_new, print_type=print_type)
                
                product_buy_cart['unit_price'] = base_price
                
                subtotal = qty * base_price
                
                product_buy_cart['subtotal'] = subtotal
                
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
            
            
        
        
        
        
        
        
        
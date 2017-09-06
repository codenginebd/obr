from datetime import datetime
from django.conf import settings

"""
Cart Structure

{
    'last_modified': datetime,
    'items': 
    {
        1213: 
        {
            'buy': 
            [
                {
                    'qty': 10,
                    'unit_price': 100,
                    'subtotal': 1000,
                    'promo_code': 'ZacdaSds',
                    'promo_amount': 200,
                    'discount_applied': True,
                    'discount_offer_type': 'amount',
                    'discount_amount': 300,
                    'total': 500,
                    'currency_code': 'BDT'
                }
            ],
            'rent': 
            [
                {
                    'qty': 10,
                    'unit_price': 100,
                    'subtotal': 1000,
                    'rent_days': 30,
                    'promo_code': 'ZacdaSds',
                    'promo_amount': 200,
                    'discount_applied': True,
                    'discount_offer_type': 'amount',
                    'discount_amount': 300,
                    'total': 500,
                    'currency_code': 'BDT'
                }
            ]
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
        
    def add_to_cart(self, buy_type, product_code, qty, unit_price, promo_applied):
        pass
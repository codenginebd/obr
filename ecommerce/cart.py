from datetime import datetime
from django.conf import settings
from book_rental.models.sales.book import Book
from enums import PromotionRewardTypes, DiscountRewardTypes
from promotion.promotion_manager import PromotionManager
from inventory.models.inventory import Inventory

"""
Cart Structure

{
    'last_modified': datetime,
    'store_credit_applied': True,
    'store_credit_amount': 100,
    'store_credit_code': 'SC-000001',
	'currency_code': 'BDT',
    'promo_applied': True,
    'promo_code': "ZPDhgdsS",
    'discount_applied': True,
	'discount_code': 'HGHGHdghsd',
	'buy':
	{
		'promo_applied': True,
		'promo_code': 'HdhshG',
		'discount_applied': True,
		'discount_code': 'HGHGHdghsd',
		1213:
		{
			'qty': 10,
			'unit_price': 100,
            'product_type': 'Book',
            'is_new': True,
            'print_type': 'ECO'
		},
		1214:
		{
			'qty': 4,
			'unit_price': 350,
            'product_type': 'Book',
            'is_new': True,
            'print_type': 'ECO'
		}
	},
	"rent":
	{
		'promo_applied': True,
		'promo_code': 'HdhshG',
		'discount_applied': True,
		'discount_code': 'HGHGHdghsd',
		1213:
		{
			'qty': 10,
			'unit_price': 100,
			'rent_days': 30,
			'rent_price': 40,
            'initial_payable': 80,
            'product_type': 'Book',
            'is_new': True,
            'print_type': 'ECO'
		},
		1214:
		{
			'qty': 1,
			'unit_price': 350,
			'rent_days': 30,
			'rent_price': 40,
            'initial_payable': 80,
            'product_type': 'Book',
            'is_new': True,
            'print_type': 'ECO'
		}
	},
	"sale":
	{
		1110:
		{
			'qty': 1,
			'good_condition': True,
			'unit_price': 40,
            'product_type': 'Book',
            'is_new': True,
            'print_type': 'ECO'
		}
	}
}

"""

class PromotionRewards(object):
    promotion_code = None
    discount_code = None
    promotion_amount = 0
    discount_amount = 0
    promotion_reward_type = PromotionRewardTypes.AMOUNT_IN_MONEY
    discount_reward_type = DiscountRewardTypes.AMOUNT_IN_MONEY
    promotion_products = []
    discount_products = []
    promotion_store_credit = 0
    discount_store_credit = 0
    

class Cart(object):
    
    def __init__(self, request, *args, **kwargs):
        if settings.CART_SESSION_ID not in request.session:
            request.session[settings.CART_SESSION_ID] = {}
        self.cart = request.session[settings.CART_SESSION_ID]
        self.request = request
        self.promotion_rewards = PromotionRewards()
        self.discount_rewards = PromotionRewards()
        self.store_credit_applied = False
        self.store_credit_amount = 0
        self.buy_items = []
        self.rent_items = []
        self.sale_items = []
        self.buy_total = 0
        self.rent_total = 0
        self.sale_total = 0
        self.subtotal = 0
        self.shipping_total = 0
        self.cart_total = 0
        self.last_updated = datetime.utcnow()
        
    def get_buy_items(self):
        return None
        
    def get_rent_items(self):
        return None
        
    def get_sale_items(self):
        return None

    def apply_store_credit(self):
        return False

    def calculate_shipping_charge(self):
        return 0
        
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
            
            
        
        
        
        
        
        
        
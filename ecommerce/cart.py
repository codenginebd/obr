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
		items:
		[
            {
                'product_id': 1213,
                'product_type': 'Book'
                'is_new': True,
                'print_type': 'ECO'
			    'qty': 10,
			    'unit_price': 100
		    }
        ]
	},
	"rent":
	{
		'promo_applied': True,
		'promo_code': 'HdhshG',
		'discount_applied': True,
		'discount_code': 'HGHGHdghsd',
		items:
		[
            {
                'product_id': 1110,
                'product_type': 'Book'
                'is_new': True,
                'print_type': 'ECO'
			    'qty': 10,
			    'unit_price': 100,
			    'rent_days': 30,
			    'rent_price': 40,
                'initial_payable': 80,
		    }
        ]
	},
	"sale":
	{
		items:
		[
            {
                'product_id': 1114,
                'product_type': 'Book',
                'is_new': True,
                'print_type': 'ECO'
			    'qty': 1,
			    'good_condition': True,
			    'unit_price': 40
		    }
        ]
	}
}

"""

class PromotionRewardProduct(object):
    product_id = None
    product_type = None
    qty = None
    is_new = None
    print_type = None
    

class PromotionRewards(object):
    promotion_code = None
    discount_code = None
    promotion_amount = 0
    discount_amount = 0
    promotion_reward_type = PromotionRewardTypes.AMOUNT_IN_MONEY
    discount_reward_type = DiscountRewardTypes.AMOUNT_IN_MONEY
    promotion_products = []  # list of PromotionRewardProduct instance
    discount_products = []  # list of PromotionRewardProduct instance
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
        self.buy_subtotal = 0
        self.buy_total = 0
        self.rent_subtotal = 0
        self.rent_total = 0
        self.sale_subtotal = 0
        self.initial_payable_subtotal = 0
        self.sale_total = 0
        self.subtotal = 0
        self.shipping_total = 0
        self.cart_total = 0
        self.return_total = 0
        self.last_updated = datetime.utcnow()
        
    def calculate_buy_subtotal(self):
        buy_cart = self.cart.get('buy', {})
        buy_items = buy_cart.get('items', [])
        buy_subtotal = 0
        for item in buy_items:
            buy_subtotal += item['unit_price']
        self.buy_subtotal = buy_subtotal
        
    def calculate_rent_subtotal(self):
        rent_cart = self.cart.get('rent', {})
        rent_items = rent_cart.get('items', [])
        rent_subtotal = 0
        for item in rent_items:
            rent_subtotal += item['rent_price']
        self.rent_subtotal = rent_subtotal
        
    def calculate_rent_initial_payable_subtotal(self):
        rent_cart = self.cart.get('rent', {})
        rent_items = rent_cart.get('items', [])
        initial_payable_subtotal = 0
        for item in rent_items:
            initial_payable_subtotal += item['initial_payable']
        self.initial_payable_subtotal = initial_payable_subtotal
        
    def calculate_sale_subtotal(self):
        sale_cart = self.cart.get('sale', {})
        sale_items = rent_cart.get('items', [])
        sale_subtotal = 0
        for item in rent_items:
            sale_subtotal += item['unit_price']
        self.sale_subtotal = sale_subtotal
        
    def perform_calculation(self):
        # Calculate Subtotals 
        self.calculate_buy_subtotal()
        self.calculate_rent_subtotal()
        self.calculate_rent_initial_payable_subtotal()
        self.calculate_sale_subtotal()
        
        
    def get_cart_total(self):
        return self.cart_total
        
    def get_buy_items(self):
        return self.buy_items
        
    def get_rent_items(self):
        return self.rent_items
        
    def get_sale_items(self):
        return self.sale_items

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
        
    def add_to_buy(self, product_id, product_type, is_new, print_type, qty, unit_price):
        buy_cart = self.cart.get('buy', {})
        buy_items = buy_cart.get('items', [])
        buy_item = {
                'product_id': product_id,
                'product_type': product_type
                'is_new': is_new,
                'print_type': print_type
			    'qty': 0,
			    'unit_price': unit_price
		    }
            
        for item in buy_items:
            if item['product_id'] == product_id and item['product_type'] == product_type and item['is_new'] == is_new and item['print_type'] == print_type:
                buy_item = item
                break
                
        buy_item['qty'] += qty
        
        buy_items += [buy_item]
        
        buy_cart['items'] = buy_items
        
        self.cart['buy'] = buy_cart
        
    def add_to_rent(self, product_id, product_type, is_new, print_type, qty, unit_price, rent_days, rent_price, initial_payable_rent):
        rent_cart = self.cart.get('rent', {})
        rent_items = rent_cart.get('items', [])
        rent_item = {
                'product_id': product_id,
                'product_type': product_type
                'is_new': is_new,
                'print_type': print_type,
			    'qty': 0,
			    'unit_price': unit_price,
			    'rent_days': rent_days,
			    'rent_price': rent_price,
                'initial_payable': initial_payable_rent,
		    }
        for item in rent_items:
            if item['product_id'] == product_id and item['product_type'] == product_type and item['is_new'] == is_new and item['print_type'] == print_type and item['rent_days'] == rent_days:
                rent_item = item
                break
                
        rent_item['qty'] += qty
        
        rent_items += [rent_item]
        
        rent_cart['items'] = rent_items
        
        self.cart['rent'] = rent_cart
        
    def add_to_sale(self, product_id, product_type, is_new, print_type, qty, unit_price, good_condition):
        sale_cart = self.cart.get('sale', {})
        sale_items = sale_cart.get('items', [])
        sale_item = {
                'product_id': product_id,
                'product_type': product_type,
                'is_new': is_new,
                'print_type': print_type,
			    'qty': 0,
			    'good_condition': good_condition,
			    'unit_price': unit_price
		    }
            
        for item in sale_items:
            if item['product_id'] == product_id and item['product_type'] == product_type and item['is_new'] == is_new and item['print_type'] == print_type:
                sale_item = item
                break
                
        sale_item['qty'] += qty
        
        sale_items += [sale_item]
        
        sale_cart['items'] = sale_items
        
        self.cart['sale'] = sale_cart
        
    def add_to_cart(self, buy_type, product_code, product_type, is_new, print_type, qty, currency_code, warehouse_id=None, rent_days=None, initial_payable_rent=None, good_condition=True):
        product_objects = Book.objects.filter(code=product_code)
        if product_objects.exists():
            product_object = product_objects.first()
            
            # Now check step by step whether to proceed or not
            
            check_rent_price = True if buy_type == 'rent' else False
            
            inventory_exists = self.check_inventory(product_id=product_object.pk, product_type=product_type, is_new=is_new, print_type=print_type, warehouse_id=warehouse_id, check_rent_available=check_rent_price)
            
            if not inventory_exists:
                return False
               
            buy_effective_price = None
            rent_unit_price = None
            rent_effective_price = None
            initial_payable_rent = None
            sale_effective_price = None
            if buy_type == 'buy':
                buy_effective_price = product_object.get_effective_base_price(is_new=is_new, print_type=print_type)
                if not buy_effective_price:
                    return False
            elif buy_type == 'rent':
                if not rent_days:
                    return False
                rent_unit_price = product_object.get_effective_base_price(is_new=is_new, print_type=print_type)
                if not rent_unit_price:
                    return False
                initial_payable_rent = product_object.get_initial_payable_rent_price(is_new=is_new, print_type=print_type)
                if not initial_payable_rent:
                    return False
                rent_effective_price = product_object.get_effective_rent_price_for_days(is_new=is_new, print_type=print_type, rent_days=rent_days)
                if not rent_effective_price:
                    return False                    
            elif buy_type == 'sale':
                sale_effective_price = product_object.get_sale_price(is_new=is_new, print_type=print_type)
                if not sale_effective_price:
                    return False        
            
            if buy_type == 'buy':
                self.add_to_buy(product_object.pk, product_type, is_new, print_type, qty, buy_effective_price)
            elif buy_type == 'rent':
                initial_payable_rent = product_object.get_initial_payable_rent_price(is_new=is_new, print_type=print_type)
                self.add_to_rent(product_object.pk, product_type, is_new, print_type, qty, rent_unit_price, rent_days, rent_effective_price, initial_payable_rent)
            elif buy_type == 'sale':
                self.add_to_sale(product_object.pk, product_type, is_new, print_type, qty, sale_effective_price, good_condition)
            
    def save(self):
        self.cart['last_modified'] = datetime.utcnow()
        self.request.session[settings.CART_SESSION_ID] = self.cart
        return self.cart
            
            
        
        
        
        
        
        
        
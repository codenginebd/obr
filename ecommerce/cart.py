from datetime import datetime
from django.conf import settings
from book_rental.models.sales.book import Book
from ecommerce.models.sales.shipping_charge import ShippingCharge
from enums import PromotionRewardTypes, DiscountRewardTypes, PromotionTypes
from promotion.models.coupon import Coupon
from promotion.models.promotion import Promotion
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
                'product_type': 'Book',
                'is_new': True,
                'print_type': 'ECO',
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
    instance = None
    code = None
    amount = 0
    reward_type = PromotionRewardTypes.AMOUNT_IN_MONEY
    products = []  # list of PromotionRewardProduct instance
    accessories = []  # list of PromotionRewardProduct instance
    store_credit = 0
    credit_expiry = None
    currency_code = None
    

class Cart(object):
    
    def __init__(self, request, *args, **kwargs):
        if settings.CART_SESSION_ID not in request.session:
            request.session[settings.CART_SESSION_ID] = {}
        self.cart = request.session[settings.CART_SESSION_ID]
        self.session_coupon_code = request.session.get(settings.SESSION_COUPON_ID, None)
        self.session_own_coupon = request.session.get(settings.SESSION_COUPON_REF, False)
        self.shipping_state = kwargs.get("shipping_state", None)
        self.shipping_zip = kwargs.get("shipping_zip", None)
        self.should_apply_store_credit = kwargs.get("apply_store_credit", False)
        self.user = request.user
        self.request = request
        self.promotion_reward = None
        self.coupon_reward = None
        self.store_credit_applied = False
        self.store_credit_amount = 0
        self.buy_items = []
        self.rent_items = []
        self.sale_items = []
        self.total_buy_products = 0
        self.total_rent_products = 0
        self.total_sale_products = 0
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
        self.currency_code = None
        self.free_shipping_applied = False
        self.last_updated = datetime.utcnow()
        
    def calculate_subtotal(self, buy_type, key_name):
        key_cart = self.cart.get('%s' % buy_type, {})
        key_items = key_cart.get('items', [])
        subtotal = 0
        for item in key_items:
            subtotal += item['%s' % key_name]
        return subtotal
        
    def calculate_buy_subtotal(self):
        self.buy_subtotal = self.calculate_subtotal('buy', 'unit_price')
        
    def calculate_rent_subtotal(self):
        self.rent_subtotal = self.calculate_subtotal('rent', 'rent_price')
        
    def calculate_rent_initial_payable_subtotal(self):
        self.initial_payable_subtotal = self.calculate_subtotal('rent', 'initial_payable')
        
    def calculate_sale_subtotal(self):
        self.sale_subtotal = self.calculate_subtotal('sale', 'unit_price')
        
    def calculate_product_count(self, buy_type):
        key_cart = self.cart.get('%s' % buy_type, {})
        key_items = key_cart.get('items', [])
        item_count = 0
        for item in key_items:
            item_count += item['qty']
        return item_count
        
    def calculate_buy_product_count(self):
        self.total_buy_products = self.calculate_product_count('buy')
        
    def calculate_rent_product_count(self):
        self.total_rent_products = self.calculate_product_count('rent')
        
    def calculate_sale_product_count(self):
        self.total_sale_products = self.calculate_product_count('sale')

    def check_list_exist(self, iter1, iter2):  # Checks if iter1 reside in iter2. iter2 is a 2d iterable
        if not iter1 or not iter2:
            return False
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

    def get_matched_iter(self, iter1, iter2, max_index):
        if not max_index:
            return None
        for index, item in enumerate(iter2):
            all_matched = []
            for i, a in enumerate(item):
                if i > max_index:
                    break
                all_matched += [item[i] == iter1[i]]
            if all(all_matched):
                return item, index

    def prepare_promotional_product_param(self, buy_type, price_key):
        if buy_type == PromotionTypes.BUY.value or buy_type == PromotionTypes.RENT.value:
            if buy_type == PromotionTypes.BUY.value:
                buy_type = "buy"
            elif buy_type == PromotionTypes.RENT.value:
                buy_type = "rent"
            key_cart = self.cart.get('%s' % buy_type, {})
            key_items = key_cart.get('items', [])
            consolidated_products = ()

            for item in key_items:
                temp_products = [list(a) for a in consolidated_products]

                tuple1 = (item['product_id'], item['product_type'], item['is_new'], item['print_type'])
                tuple2 = consolidated_products
                matched_tuple, matched_index = self.get_matched_iter(tuple1, tuple2, 3)
                if matched_tuple:
                    current_subtotal = matched_tuple[6]
                    subtotal = item['qty'] * item['%s' % price_key]
                    new_subtotal = current_subtotal + subtotal
                    temp_products[matched_index] = list(tuple1) + [item['qty'], item['%s' % price_key], new_subtotal]
                else:
                    subtotal = item['qty'] * item['%s' % price_key]
                    temp_products += list(tuple1) + [item['qty'], item['%s' % price_key], subtotal]

            consolidated_products = tuple([tuple(t) for t in temp_products])

            return consolidated_products
        elif buy_type == PromotionTypes.ANY.value:
            buy_cart = self.cart.get("buy", {})
            rent_cart = self.cart.get("rent", {})
            buy_items = buy_cart.get("items", [])
            rent_items = rent_cart.get("items", [])
            any_items = []
            for item in buy_items:
                any_items += [
                    {
                        'product_id': item['product_id'],
                        'product_type': item['product_type'],
                        'is_new': item['is_new'],
                        'print_type': item['print_type'],
                        'qty': item['qty'],
                        'unit_price': item['unit_price']
                    }
                ]

            for item in rent_items:
                any_items += [
                    {
                        'product_id': item['product_id'],
                        'product_type': item['product_type'],
                        'is_new': item['is_new'],
                        'print_type': item['print_type'],
                        'qty': item['qty'],
                        'unit_price': item['rent_price']
                    }
                ]
            consolidated_products = ()

            for item in any_items:
                temp_products = [list(a) for a in consolidated_products]

                tuple1 = (item['product_id'], item['product_type'], item['is_new'], item['print_type'])
                tuple2 = consolidated_products
                matched_tuple, matched_index = self.get_matched_iter(tuple1, tuple2, 3)
                if matched_tuple:
                    current_subtotal = matched_tuple[6]
                    subtotal = item['qty'] * item['unit_price']
                    new_subtotal = current_subtotal + subtotal
                    temp_products[matched_index] = list(tuple1) + [item['qty'], item['unit_price'], new_subtotal]
                else:
                    subtotal = item['qty'] * item['unit_price']
                    temp_products += list(tuple1) + [item['qty'], item['unit_price'], subtotal]

            consolidated_products = tuple([tuple(t) for t in temp_products])
            return consolidated_products

    def get_promotions_by_type(self, promotion_type, price_key, best):
        product_params = self.prepare_promotional_product_param(promotion_type, price_key)
        promotional_rewards = Promotion.get_promotional_rewards(promotion_type=promotion_type,
                                                                cart_total=self.buy_subtotal,
                                                                total_items=self.total_buy_products,
                                                                cart_products=product_params, best=best)
        return promotional_rewards

    def apply_promotional_reward(self, reward, promotion_type):
        if promotion_type not in [PromotionTypes.BUY.value, PromotionTypes.RENT.value,PromotionTypes.ANY.value]:
            return None
        if not reward['promo_codes']:
            return False

        if not reward["promotion_instances"]:
            return False

        promo_instance = reward["promotion_instances"][0]
        promo_code = reward['promo_codes'][0]
        amount = reward['amount']
        free_shipping = reward['free_shipping']
        free_products = reward['free_products']
        accessories = reward['accessories']
        store_credit = reward['store_credit']
        credit_expiry = reward['credit_expiry']
        currency_code = reward["currency_code"]

        self.promotion_reward = PromotionRewards()
        self.promotion_reward.instance = promo_instance
        self.promotion_reward.code = promo_code
        if amount > 0:
            self.promotion_reward.reward_type = PromotionRewardTypes.AMOUNT_IN_MONEY.value
            self.promotion_reward.amount = amount

        if free_shipping:
            self.promotion_reward.reward_type = PromotionRewardTypes.FREE_SHIPPING.value

        if free_products:
            for free_product in free_products:
                reward_product = PromotionRewardProduct()
                reward_product.product_id = free_product['product_id']
                reward_product.product_type = free_product['product_model']
                reward_product.is_new = free_product['is_new']
                reward_product.print_type = free_product['print_type']
                reward_product.qty = free_product['quantity']
                self.promotion_reward.products += [reward_product]

        if accessories:
            for accessory in accessories:
                reward_product = PromotionRewardProduct()
                reward_product.product_id = accessory['product_id']
                reward_product.product_type = accessory['product_model']
                reward_product.is_new = accessory['is_new']
                reward_product.print_type = accessory['print_type']
                reward_product.qty = accessory['quantity']
                self.promotion_reward.accessories += [reward_product]

        if store_credit:
            self.promotion_reward.store_credit = store_credit
            self.promotion_reward.credit_expiry = credit_expiry

        if promotion_type == PromotionTypes.ANY.value:
            if not self.currency_code:
                self.currency_code = currency_code
        else:
            if not self.promotion_reward.currency_code:
                self.promotion_reward.currency_code = currency_code

    def apply_best_promotion(self):
        # Buy Promotions
        promotional_rewards = self.get_promotions_by_type(promotion_type=PromotionTypes.BUY.value,
                                                          price_key='unit_price', best=True)

        if promotional_rewards:
            promotional_reward = promotional_rewards[0]
            self.apply_promotional_reward(promotional_reward, promotion_type=PromotionTypes.BUY.value)

        # Rent Promotions
        promotional_rewards = self.get_promotions_by_type(promotion_type=PromotionTypes.RENT.value,
                                                          price_key='rent_price', best=True)
        if promotional_rewards:
            promotional_reward = promotional_rewards[0]
            self.apply_promotional_reward(promotional_reward, promotion_type=PromotionTypes.RENT.value)

        # Any Promotions
        promotional_rewards = self.get_promotions_by_type(promotion_type=PromotionTypes.ANY.value,
                                                          price_key=None, best=True)
        if promotional_rewards:
            promotional_reward = promotional_rewards[0]
            self.apply_promotional_reward(promotional_reward, promotion_type=PromotionTypes.ANY.value)

    def get_coupons_by_type(self, coupon_type):
        if not self.session_coupon_code:
            return False
        referrer_id = None
        if self.session_own_coupon:
            if not self.user.is_authenticate():
                return False
            else:
                referrer_id = self.user.pk
        else:
            referrer_id = None

        cart_total = None
        if coupon_type == PromotionTypes.BUY.value:
            cart_total = self.buy_subtotal
        elif coupon_type == PromotionTypes.RENT.value:
            cart_total = self.rent_subtotal
        elif coupon_type == PromotionTypes.ANY.value:
            cart_total = self.buy_subtotal + self.rent_subtotal

        if cart_total:
            coupon_rewards = Coupon.get_coupon_rewards(coupon_code=self.session_coupon_code,
                                      coupon_type=coupon_type,
                                      cart_total=cart_total,referrer_id=referrer_id, best=True)
            return coupon_rewards

    def apply_coupon_reward(self, reward, coupon_type):
        if coupon_type not in [PromotionTypes.BUY.value, PromotionTypes.RENT.value, PromotionTypes.ANY.value]:
            return None
        if not reward['coupon_code']:
            return False

        if not reward['coupon_instance']:
            return False

        coupon_instance = reward['coupon_instance']
        coupon_code = reward['coupon_code']
        amount = reward['amount']
        free_shipping = reward['free_shipping']
        free_products = reward['free_products']
        accessories = reward['accessories']
        store_credit = reward['store_credit']
        credit_expiry = reward['credit_expiry']
        currency_code = reward["currency_code"]

        self.coupon_reward = PromotionRewards()
        self.coupon_reward.instance = coupon_instance
        self.coupon_reward.code = coupon_code
        if amount > 0:
            self.coupon_reward.reward_type = PromotionRewardTypes.AMOUNT_IN_MONEY.value
            self.coupon_reward.amount = amount

        if free_shipping:
            self.coupon_reward.reward_type = PromotionRewardTypes.FREE_SHIPPING.value

        if free_products:
            for free_product in free_products:
                reward_product = PromotionRewardProduct()
                reward_product.product_id = free_product['product_id']
                reward_product.product_type = free_product['product_model']
                reward_product.is_new = free_product['is_new']
                reward_product.print_type = free_product['print_type']
                reward_product.qty = free_product['quantity']
                self.coupon_reward.products += [reward_product]

        if accessories:
            for accessory in accessories:
                reward_product = PromotionRewardProduct()
                reward_product.product_id = accessory['product_id']
                reward_product.product_type = accessory['product_model']
                reward_product.is_new = accessory['is_new']
                reward_product.print_type = accessory['print_type']
                reward_product.qty = accessory['quantity']
                self.coupon_reward.accessories += [reward_product]

        if store_credit:
            self.coupon_reward.store_credit = store_credit
            self.coupon_reward.credit_expiry = credit_expiry

        if coupon_type == PromotionTypes.ANY.value:
            if not self.currency_code:
                self.currency_code = currency_code
        else:
            if not self.promotion_reward.currency_code:
                self.coupon_reward.currency_code = currency_code

    def apply_best_coupon(self):
        coupon_rewards = self.get_coupons_by_type(coupon_type=PromotionTypes.BUY.value)
        if coupon_rewards:
            coupon_reward = coupon_rewards[0]
            self.apply_coupon_reward(reward=coupon_reward, coupon_type=PromotionTypes.BUY.value)

        coupon_rewards = self.get_coupons_by_type(coupon_type=PromotionTypes.RENT.value)
        if coupon_rewards:
            coupon_reward = coupon_rewards[0]
            self.apply_coupon_reward(reward=coupon_reward, coupon_type=PromotionTypes.RENT.value)

        coupon_rewards = self.get_coupons_by_type(coupon_type=PromotionTypes.ANY.value)
        if coupon_rewards:
            coupon_reward = coupon_rewards[0]
            self.apply_coupon_reward(reward=coupon_reward, coupon_type=PromotionTypes.ANY.value)

    def get_best_reward_score(self, total, rewards, best_score=0):
        new_best = False
        total_reward_score = 0
        rewards = self.promotion_reward.instance.rewards.all()
        for reward in rewards:
            total_reward_score += reward.get_reward_weight(cart_total=total)
        if total_reward_score > best_score:
            best_score = total_reward_score
        return best_score

    def apply_best_among_promotion_coupon(self):
        best_score1 = 0
        best_score2 = 0
        if self.promotion_reward:
            if self.promotion_reward.instance:
                if self.promotion_reward.instance.promotion_type == PromotionTypes.BUY.value:
                    best_score1 = self.get_best_reward_score(total=self.buy_subtotal,
                                                            rewards=self.promotion_reward.instance.rewards.all(),
                                                            best_score=best_score1)
                elif self.promotion_reward.instance.promotion_type == PromotionTypes.RENT.value:
                    best_score1 = self.get_best_reward_score(total=self.rent_subtotal,
                                                            rewards=self.promotion_reward.instance.rewards.all(),
                                                            best_score=best_score1)
                elif self.promotion_reward.instance.promotion_type == PromotionTypes.ANY.value:
                    best_score1 = self.get_best_reward_score(total=self.subtotal,
                                                            rewards=self.promotion_reward.instance.rewards.all(),
                                                            best_score=best_score1)

        if self.coupon_reward:
            if self.coupon_reward.instance:
                if self.coupon_reward.instance.coupon_type == PromotionTypes.BUY.value:
                    best_score2 = self.get_best_reward_score(total=self.buy_subtotal,
                                                                       rewards=self.promotion_reward.instance.rewards.all(),
                                                                       best_score=best_score2)
                elif self.promotion_reward.instance.promotion_type == PromotionTypes.RENT.value:
                    best_score2 = self.get_best_reward_score(total=self.rent_subtotal,
                                                                       rewards=self.promotion_reward.instance.rewards.all(),
                                                                       best_score=best_score2)
                elif self.promotion_reward.instance.promotion_type == PromotionTypes.ANY.value:
                    best_score2 = self.get_best_reward_score(total=self.subtotal,
                                                                       rewards=self.promotion_reward.instance.rewards.all(),
                                                                       best_score=best_score2)

        if best_score1 >= best_score2:
            self.coupon_reward = None
        elif best_score1 < best_score2:
            self.promotion_reward = None

    def apply_coupon_promotions_to_cart_type_total(self):
        if self.promotion_reward:
            if self.promotion_reward.reward_type == PromotionRewardTypes.AMOUNT_IN_MONEY.value:
                if self.promotion_reward.instance.promotion_type == PromotionTypes.BUY.value:
                    if self.promotion_reward.instance.amount >= 0:
                        buy_total = self.buy_subtotal - self.promotion_reward.instance.amount
                        if buy_total < 0:
                            buy_total = 0
                        self.buy_total = buy_total
                elif self.promotion_reward.instance.promotion_type == PromotionTypes.RENT.value:
                    if self.promotion_reward.instance.amount >= 0:
                        rent_total = self.rent_subtotal - self.promotion_reward.instance.amount
                        if rent_total < 0:
                            rent_total = 0
                        self.rent_total = rent_total

        if self.coupon_reward:
            if self.coupon_reward.reward_type == PromotionRewardTypes.AMOUNT_IN_MONEY.value:
                if self.coupon_reward.instance.promotion_type == PromotionTypes.BUY.value:
                    if self.coupon_reward.instance.amount >= 0:
                        buy_total = self.buy_total - self.promotion_reward.instance.amount
                        if buy_total < 0:
                            buy_total = 0
                        self.buy_total = buy_total
                elif self.coupon_reward.instance.promotion_type == PromotionTypes.RENT.value:
                    if self.coupon_reward.instance.amount >= 0:
                        rent_total = self.rent_total - self.promotion_reward.instance.amount
                        if rent_total < 0:
                            rent_total = 0
                        self.rent_total = rent_total

    def get_store_credits(self):
        store_credits = {}
        if self.promotion_reward:
            if self.promotion_reward.reward_type == PromotionRewardTypes.STORE_CREDIT.value:
                store_credits[self.promotion_reward.credit_expiry] = self.promotion_reward.store_credit

        if self.coupon_reward:
            if self.coupon_reward.reward_type == PromotionRewardTypes.STORE_CREDIT.value:
                if self.promotion_reward.credit_expiry in store_credits.keys():
                    store_credits[self.promotion_reward.credit_expiry] += self.promotion_reward.store_credit
                else:
                    store_credits[self.promotion_reward.credit_expiry] = self.promotion_reward.store_credit
        return store_credits

    def apply_store_credit(self):
        pass

    def calculate_shipping_charge(self):
        if self.promotion_reward:
            if self.promotion_reward.reward_type == PromotionRewardTypes.FREE_SHIPPING.value:
                self.free_shipping_applied = True
        if self.coupon_reward:
            if self.coupon_reward.reward_type == PromotionRewardTypes.FREE_SHIPPING.value:
                self.free_shipping_applied = True

        if not self.free_shipping_applied:
            if self.shipping_state:
                shipping_charge = None
                if self.shipping_zip:
                    shipping_charge = ShippingCharge.get_shipping_charge(shipping_state=self.shipping_state,
                                                       total_amount=self.subtotal, zip_code=self.shipping_zip)
                else:
                    shipping_charge = ShippingCharge.get_shipping_charge(shipping_state=self.shipping_state,
                                                       total_amount=self.subtotal, zip_code=self.shipping_zip)
                if shipping_charge:
                    self.shipping_total = shipping_charge
        
    def calculate_total(self):
        total = self.buy_total
        if total < 0:
            total = 0

        if self.rent_total > 0:
            total += self.rent_total

        self.subtotal = total

    def apply_coupon_promotions_in_cart_total(self):
        if self.promotion_reward:
            if self.promotion_reward.reward_type == PromotionRewardTypes.AMOUNT_IN_MONEY.value:
                if self.promotion_reward.instance.promotion_type == PromotionTypes.ANY.value:
                    if self.promotion_reward.instance.amount >= 0:
                        subtotal = self.subtotal - self.promotion_reward.instance.amount
                        if subtotal < 0:
                            subtotal = 0
                        self.subtotal = subtotal

        if self.coupon_reward:
            if self.coupon_reward.reward_type == PromotionRewardTypes.AMOUNT_IN_MONEY.value:
                if self.coupon_reward.instance.promotion_type == PromotionTypes.ANY.value:
                    if self.coupon_reward.instance.amount >= 0:
                        subtotal = self.subtotal - self.coupon_reward.instance.amount
                        if subtotal < 0:
                            subtotal = 0
                        self.subtotal = subtotal

    def calculate_grand_total(self):
        if self.promotion_reward.reward_type == PromotionRewardTypes.FREE_SHIPPING.value \
                or self.coupon_reward.reward_type == PromotionRewardTypes.FREE_SHIPPING.value:
            self.cart_total = self.subtotal
        else:
            if self.shipping_total > 0:
                cart_total = self.subtotal + self.shipping_total
                if cart_total > 0:
                    self.cart_total = cart_total
                else:
                    self.cart_total = 0
            else:
                self.cart_total = self.subtotal

    def calculate_total_rent_return(self):
        if self.initial_payable_subtotal:
            total_return = self.initial_payable_subtotal - self.rent_total
            if total_return > 0:
                self.return_total =  total_return
        
    def perform_calculation(self):
        self.calculate_buy_product_count()
        self.calculate_rent_product_count()
        self.calculate_sale_product_count()
        self.calculate_buy_subtotal()
        self.calculate_rent_subtotal()
        self.calculate_rent_initial_payable_subtotal()
        self.calculate_sale_subtotal()
        self.apply_best_promotion()
        self.apply_best_coupon()
        if settings.APPLY_BEST_COUPON_PROMO:
            self.apply_best_among_promotion_coupon()
        self.apply_coupon_promotions_to_cart_type_total()
        self.calculate_total()
        self.calculate_total_rent_return()
        self.apply_coupon_promotions_in_cart_total()
        if self.should_apply_store_credit:
            self.apply_store_credit()
        self.calculate_shipping_charge()
        self.calculate_grand_total()
        
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
            'product_type': product_type,
            'is_new': is_new,
            'print_type': print_type,
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
            'product_type': product_type,
            'is_new': is_new,
            'print_type': print_type,
            'qty': 0,
            'unit_price': unit_price,
            'rent_days': rent_days,
            'rent_price': rent_price,
            'initial_payable': initial_payable_rent
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

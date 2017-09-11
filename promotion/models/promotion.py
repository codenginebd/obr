from datetime import datetime
from django.db import models, transaction
from enums import PROMOTION_REWARD_TYPES
from generics.models.base_entity import BaseEntity
from promotion.models.promotion_products_rule import PromotionProductRule
from promotion.models.promotion_reward import PromotionReward
from promotion.model_managers import PromotionManagerByQuantity, PromotionManagerByAmount, PromotionManagerByProducts
from promotion.models.promotion_reward_products import PromotionRewardProduct

"""
Based on by_amount or by_
quantity set to True either min_qty
or min_amount will have value

1. Buy 1 Get 1
2. Buy more than 500 BDT and get free shippping
3. Buy more than 3 items of X and get one Y item Free
4. Buy from 11th Sep to 15th Sep and Get free shipping

"""


class Promotion(BaseEntity):
    title = models.CharField(max_length=200)
    description = models.TextField(default='')

    by_cart = models.BooleanField(default=False)  # Either by_cart or by_products or by_dates will be True not all
    by_products = models.BooleanField(default=False)
    by_dates = models.BooleanField(default=False)

    by_amount = models.BooleanField(default=False)  # Either by_amount or by_quantity will be True not both
    by_quantity = models.BooleanField(default=False)

    min_qty = models.IntegerField(default=0)
    min_amount = models.DecimalField(max_digits=20, decimal_places=2)

    product_rules = models.ManyToManyField(PromotionProductRule)  # If by_products is set then this will have entries

    rewards = models.ManyToManyField(PromotionReward)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    
    objects_by_quantity = PromotionManagerByQuantity()
    objects_by_amount = PromotionManagerByAmount()
    objects_by_products = PromotionManagerByProducts()

    """
    cart_total = 500
    cart_products = [ ( product_id, product_type, qty, unit_price, subtotal ) ]
    """
    @classmethod
    def get_promotions(cls, cart_total, cart_products=[], **kwargs):

        return []

    """
    by_cart_products_dates = "BY_CART", "BY_PRODUCTS", "BY_DATE"
    by_amount_qty = "BY_AMOUNT", "BY_QTY"
    min_qty_amount = "MIN_QTY", "MIN_AMOUNT"
    products = [ ( ID, TYPE, min_qty_amount ) ]
    rewards = [ ( REWARD_TYPE, GIFT_AMOUNT, store_credit, credit_expiry_time,
        products=[ ( ID, TYPE, quantity ) ] ) ]
    """
    @classmethod
    def create_or_update_promotion(cls, title, description, start_date, end_date, by_cart_products_dates,
                         by_amount_qty, min_qty_amount, products=[], rewards=[], **kwargs):
        by_cart_products_dates_options = [ "BY_CART", "BY_PRODUCTS", "BY_DATE" ]
        by_amount_qty_options = [ "BY_AMOUNT", "BY_QTY" ]
        min_qty_amount_options = [ "MIN_QTY", "MIN_AMOUNT" ]
        with transaction.atomic():
            try:
                if len(title) > 200:
                    return False
                if len(description) > 500:
                    return False
                if by_cart_products_dates not in by_cart_products_dates_options:
                    return False
                if by_amount_qty not in by_amount_qty_options:
                    return False
                if not all([True for row in products if len(row) == 3]):
                    return False
                if not all([True for row in rewards if len(row) == 5]):
                    return False
                for reward in rewards:
                    if reward[0] not in [ PROMOTION_REWARD_TYPES.AMOUNT_IN_MONEY.value,
                                          PROMOTION_REWARD_TYPES.FREE_SHIPPING.value,
                                          PROMOTION_REWARD_TYPES.FREE_PRODUCTS.value,
                                          PROMOTION_REWARD_TYPES.ACCESSORIES.value,
                                          PROMOTION_REWARD_TYPES.STORE_CREDIT.value]:
                        return False
                    if not all([True for r in reward[4] if len(r) == 3]):
                        return False

                # validation done. Now proceed to create promotion

                pk = kwargs.get('pk')
                if pk:
                    promotion_objects = cls.objects.filter(pk=pk)
                    promotion_object = promotion_objects.first()
                else:
                    promotion_object = cls()

                promotion_object.title = title
                promotion_object.description = description
                promotion_object.start_date = start_date
                promotion_object.end_date = end_date

                if by_cart_products_dates == "BY_CART":
                    promotion_object.by_cart = True
                elif by_cart_products_dates == "BY_PRODUCTS":
                    promotion_object.by_products = True
                elif by_cart_products_dates == "BY_DATE":
                    promotion_object.by_dates = True

                if by_amount_qty == "BY_AMOUNT":
                    promotion_object.by_amount = True
                    promotion_object.min_amount = min_qty_amount
                elif by_amount_qty == "BY_QTY":
                    promotion_object.by_quantity = True
                    promotion_object.min_qty = min_qty_amount

                promotion_object.save()

                if pk:
                    if promotion_object.product_rules.exists():
                        product_rules = promotion_object.product_rules.all()
                        promotion_object.product_rules.clear()
                        product_rules.delete()

                if by_cart_products_dates == "BY_PRODUCTS":
                    product_rule_objects = []
                    for product_rule in products:
                        product_id = product_rule[0]
                        product_type = product_rule[1]
                        min_qty_amount = product_rule[2]

                        product_rule_object = PromotionProductRule()
                        product_rule_object.product_id = product_id
                        product_rule_object.product_model = product_type
                        if by_amount_qty == "BY_AMOUNT":
                            product_rule_object.min_amount = min_qty_amount
                        elif by_amount_qty == "BY_QTY":
                            product_rule_object.min_qty = min_qty_amount

                        product_rule_object.save()

                        product_rule_objects += [ product_rule_object ]

                    promotion_object.product_rules.add(*product_rule_objects)

                # Add Promotion Rewards

                if pk:
                    if promotion_object.rewards.exists():
                        promotion_rewards = promotion_object.rewards.all()
                        promotion_object.rewards.clear()
                        promotion_rewards.delete()

                promo_rewards = []
                for reward in rewards:
                    reward_type = reward[0]
                    gift_amount = reward[1]
                    store_credit = reward[2]
                    credit_expiry_datetime = reward[3]
                    products = reward[4]
                    accessories = reward[5]

                    reward_object = PromotionReward()
                    reward_object.reward_type = reward_type
                    if reward_type == PROMOTION_REWARD_TYPES.AMOUNT_IN_MONEY.value:
                        reward_object.gift_amount = gift_amount
                    elif reward_type == PROMOTION_REWARD_TYPES.FREE_SHIPPING.value:
                        pass
                    elif reward_type == PROMOTION_REWARD_TYPES.FREE_PRODUCTS.value or reward_type == PROMOTION_REWARD_TYPES.ACCESSORIES.value:
                        reward_object.save()

                        promo_reward_product_instances = reward_object.products.all()
                        reward_object.products.clear()
                        promo_reward_product_instances.delete()

                        promo_reward_products = []
                        for reward_product_row in products:
                            pid = reward_product_row[0]
                            ptype = reward_product_row[1]
                            pquantity = reward_product_row[2]

                            promo_reward_product = PromotionRewardProduct()
                            promo_reward_product.product_id = pid
                            promo_reward_product.product_model = ptype
                            promo_reward_product.quantity = pquantity
                            promo_reward_product.save()

                            promo_reward_products += [ promo_reward_product ]

                        reward_object.products.add(*promo_reward_products)

                    elif reward_type == PROMOTION_REWARD_TYPES.STORE_CREDIT.value:
                        reward_object.store_credit = store_credit
                        reward_object.credit_expiry_time = credit_expiry_datetime

                    reward_object.save()

                    promo_rewards += [ reward_object ]

                promotion_object.rewards.add(*promo_rewards)


            except Exception as exp:
                return False
    
    
    
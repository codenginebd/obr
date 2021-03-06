from datetime import datetime
from django.db import models, transaction
from django.db.models.query_utils import Q
from django.urls.base import reverse

from enums import PromotionRewardTypes, PromotionTypes
from generics.models.base_entity import BaseEntity
from payment.models.currency import Currency
from promotion.models.promotion_products_rule import PromotionProductRule
from promotion.models.promotion_reward import PromotionReward
from promotion.model_managers import PromotionManagerByQuantity, PromotionManagerByAmount, PromotionManagerByProducts
from promotion.models.promotion_reward_products import PromotionRewardProduct

"""
Based on by_amount or by_
quantity set to True either min_qty
or min_amount will have value

1. Buy 1 Get 1
2. Buy more than 500 BDT and get free shipping
3. Buy more than 3 items of X and get one Y item Free
4. Buy from 11th Sep to 15th Sep and Get free shipping

"""


class Promotion(BaseEntity):
    title = models.CharField(max_length=200)
    description = models.TextField(default='')

    promotion_type = models.IntegerField(default=PromotionTypes.BUY.value)

    by_cart = models.BooleanField(default=False)  # Either by_cart or by_products or by_dates will be True not all
    by_products = models.BooleanField(default=False)
    by_dates = models.BooleanField(default=False)

    by_amount = models.BooleanField(default=False)  # Either by_amount or by_quantity will be True not both
    by_quantity = models.BooleanField(default=False)

    min_qty = models.IntegerField(default=0)
    min_amount = models.DecimalField(max_digits=20, decimal_places=2,default=0.0)

    product_rules = models.ManyToManyField(PromotionProductRule)  # If by_products is set then this will have entries

    rewards = models.ManyToManyField(PromotionReward)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    
    # objects_by_quantity = PromotionManagerByQuantity()
    # objects_by_amount = PromotionManagerByAmount()
    # objects_by_products = PromotionManagerByProducts()

    def get_promotion_type(self):
        if self.promotion_type == PromotionTypes.BUY.value:
            return "Buy"
        elif self.promotion_type == PromotionTypes.RENT.value:
            return "Rent"
        elif self.promotion_type == PromotionTypes.ANY.value:
            return "Any"

    @classmethod
    def show_create(cls):
        return True

    @classmethod
    def show_edit(cls):
        return True

    @classmethod
    def get_create_link(cls):
        return reverse("admin_promotion_create_view")

    @classmethod
    def get_table_headers(self):
        return ["Id", "Code", "Title", "Promotion Type", "Start Date", "Expiry Date", "Details"]

    @classmethod
    def prepare_table_data(cls, queryset):
        data = []
        for q_object in queryset:
            data += [
                [q_object.pk, q_object.code, q_object.title, q_object.get_promotion_type(),
                 q_object.start_date.strftime("%d/%m/%Y") if q_object.start_date else "",
                 q_object.end_date.strftime("%d/%m/%Y") if q_object.end_date else "",
                 '<a href="%s">Details</a>' % q_object.get_detail_link(object_id=q_object.pk)]
            ]
        return data


    def get_code_prefix(self):
        return "PROMO"

    @classmethod
    def find_the_best_promotion(cls, promotions, cart_total):
        best_promotion = None
        first_promotion = promotions.first()
        best_promo_weight = 0
        for promotion in promotions:
            promo_reward_weight = 0
            rewards = promotion.rewards.all()
            for reward in rewards:
                reward_weight = reward.get_reward_weight(cart_total=cart_total)
                if reward_weight:
                    promo_reward_weight += reward_weight
            if promo_reward_weight > best_promo_weight:
                best_promo_weight = promo_reward_weight
                best_promotion = promotion
        if best_promotion:
            return promotions.filter(pk=best_promotion.pk)
        else:
            return promotions.filter(pk=first_promotion.pk)

    """
    cart_total = 500
    total_items = 100,
    cart_products = [ ( product_id, product_type, is_new, print_type, qty, unit_price, subtotal ),
                      ( 1, "Book", True, "ECO", 2, 120, 240 ),
                      ( 2, "Book", True, "ECO", 1, 300, 300 )],
    best = True
                      
    Returns:
    
    {
        "promotion_instances": [],
        "promo_codes": [],
        "amount": 0,
        "currency_code": "BDT",
        "free_shipping": False,
        "free_products": 
        [
             {
                "product_id": 1,
                "product_model": "Book",
                "is_new": True,
                "print_type": "ECO",
                "quantity": 4
            }
        ],
        "accessories": 
        [
             {
                "product_id": 1,
                "product_model": "Book",
                "is_new": True,
                "print_type": "ECO",
                "quantity": 4
            }
        ],
        'store_credit': 0,
        'credit_expiry': None
    }
                      
    """
    @classmethod
    def get_promotional_rewards(cls, promotion_type, cart_total, total_items, cart_products=[], best=True, **kwargs):
        promotional_rewards = {
            "promotion_instances": [],
            "promo_codes": [],
            "amount": 0,
            "currency_code": None,
            "free_shipping": False,
            "free_products": [],
            "accessories": [],
            "store_credit": 0,
            "credit_expiry": None
        }
        all_promotions = cls.get_promotions(promotion_type, cart_total, total_items, cart_products=cart_products, **kwargs)
        if best:
            # Find the best promotion and then get rewards
            all_promotions = cls.find_the_best_promotion(promotions=all_promotions, cart_total=cart_total)
        if all_promotions:
            all_reward_ids = []
            for promotion_instance in all_promotions:
                promotional_rewards["promotion_instances"] += [promotion_instance]
                promotional_rewards["promo_codes"] += [promotion_instance.code]
                promotional_rewards["currency_code"] = promotion_instance.currency.short_name
                all_reward_ids += promotion_instance.rewards.values_list('pk', flat=True)
                
            if all_reward_ids:
                all_rewards = PromotionReward.objects.filter(pk__in=all_reward_ids)
                for reward_instance in all_rewards:
                    if reward_instance.reward_type == PromotionRewardTypes.AMOUNT_IN_MONEY.value:
                        if reward_instance.gift_amount_in_percentage:
                            promotional_rewards["amount"] += reward_instance.gift_amount * cart_total
                        else:
                            promotional_rewards["amount"] += reward_instance.gift_amount
                    elif reward_instance.reward_type == PromotionRewardTypes.FREE_SHIPPING.value:
                        promotional_rewards["free_shipping"] = True
                    elif reward_instance.reward_type == PromotionRewardTypes.FREE_PRODUCTS.value:
                        for reward_product in reward_instance.products.all():
                            promotional_rewards["free_products"] += [
                                {
                                    "product_id": reward_product.product_id,
                                    "product_model": reward_product.product_model,
                                    "is_new": reward_product.is_new,
                                    "print_type": reward_product.print_type,
                                    "quantity": reward_product.quantity
                                }
                            ]
                    elif reward_instance.reward_type == PromotionRewardTypes.ACCESSORIES.value:
                        for reward_product in reward_instance.products.all():
                            promotional_rewards["free_products"] += [
                                {
                                    "product_id": reward_product.product_id,
                                    "product_model": reward_product.product_model,
                                    "quantity": reward_product.quantity
                                }
                            ]
                    elif reward_instance.reward_type == PromotionRewardTypes.STORE_CREDIT.value:
                        promotional_rewards["store_credit"] += reward_instance.store_credit
                        promotional_rewards["credit_expiry"] = reward_instance.credit_expiry_time
                return promotional_rewards
            else:
                return None
            
        else:
            return None

    """
    promotion_type = PROMOTION_TYPES.BUY.value
    cart_total = 500
    total_items = 100,
    cart_products = [ ( product_id, product_type, is_new, print_type, qty, unit_price, subtotal ),
                      ( 1, "Book", True, "ECO", 2, 120, 240 ),
                      ( 2, "Book", True, "ORI", 1, 300, 300 )]
    """
    @classmethod
    def get_promotions(cls, promotion_type, cart_total, total_items, cart_products=[], **kwargs):
        try:
            if not all([True for row in cart_products if len(row) == 7]):
                return False

            now_date = datetime.utcnow().date()

            all_promotions_by_dates_expressions = (Q(by_dates=True) & Q(start_date__lte=now_date) & Q(end_date__gte=now_date))

            all_promotions_by_cart_expressions = ((Q(by_cart=True) &
                                                   ((Q(by_quantity=True) & Q(min_qty__lte=total_items)) |
                                                    (Q(by_amount=True) & Q(min_amount__lte=cart_total)))) &
                                                  Q(start_date__lte=now_date) & Q(end_date__gte=now_date))

            # Get all promotion product rules
            promotion_product_query_expression = None
            for cart_product in cart_products:
                product_id = cart_product[0]
                product_type = cart_product[1]
                is_new = cart_product[2]
                print_type = cart_product[3]
                product_qty = cart_product[4]
                product_unit_price = cart_product[5]
                product_subtotal = cart_product[6]

                qry_expression = ((Q(product_id=product_id) & Q(product_model=product_type) & Q(is_new=is_new) & Q(print_type=print_type) & 
                                   Q(min_qty__lte=product_qty) & Q(min_amount=0)) |
                                  (Q(product_id=product_id) & Q(product_model=product_type) & Q(is_new=is_new) & Q(print_type=print_type) & 
                                   Q(min_amount__lte=product_subtotal) & Q(min_qty=0)))

                if promotion_product_query_expression:
                    promotion_product_query_expression |= qry_expression
                else:
                    promotion_product_query_expression = qry_expression

            promotion_product_pks = []
            if promotion_product_query_expression:
                promotion_product_pks = PromotionProductRule.objects.filter(promotion_product_query_expression).values_list('pk', flat=True).distinct()

            if promotion_product_pks:
                all_promotions_by_products_expressions = ((Q(by_products=True) & Q(product_rules__id__in=promotion_product_pks)) & Q(start_date__lte=now_date) & Q(end_date__gte=now_date))
            else:
                all_promotions_by_products_expressions = None

            all_promotions_expresions = all_promotions_by_dates_expressions | all_promotions_by_cart_expressions
        
            if all_promotions_by_products_expressions:
                all_promotions_expresions |= all_promotions_by_products_expressions
        
            all_promotion_ids = cls.objects.filter(promotion_type=promotion_type).filter(all_promotions_expresions).values_list('pk', flat=True).distinct()

            all_promotions = cls.objects.filter(pk__in=all_promotion_ids)

            return all_promotions
        except Exception as exp:
            return None

    """
    title,
    description,
    start_date,
    end_date,
    promotion_type = "BUY",
    by_cart_products_dates = "BY_CART", "BY_PRODUCTS", "BY_DATE"
    by_amount_qty = "BY_AMOUNT", "BY_QTY"
    min_qty_amount = 100
    products = [ ( ID, TYPE, is_new, print_type, min_qty_amount ) ]
    rewards = [ ( REWARD_TYPE, gift_amount_in_percentage, GIFT_AMOUNT, store_credit, credit_expiry_time,
        products=[ ( ID, TYPE, quantity, is_new, print_type ) ] ) ]
    """
    @classmethod
    def create_or_update_promotion(cls, title, description, start_date, end_date,
                                   promotion_type, by_cart_products_dates,by_amount_qty, min_qty_amount, currency_code,
                                   products=[], rewards=[], **kwargs):
        by_cart_products_dates_options = ["BY_CART", "BY_PRODUCTS", "BY_DATE"]
        by_amount_qty_options = ["BY_AMOUNT", "BY_QTY"]
        promotion_type_options = ["BUY", "RENT", "ANY"]
        currency_objects = Currency.objects.filter(short_name=currency_code)
        if not currency_objects.exists():
            return False
        currency_object = currency_objects.first()
        with transaction.atomic():
            try:
                if len(title) > 200:
                    return False
                if len(description) > 500:
                    return False
                if promotion_type not in promotion_type_options:
                    return False
                if by_cart_products_dates not in by_cart_products_dates_options:
                    return False
                if by_amount_qty not in by_amount_qty_options:
                    return False
                if not all([True for row in products if len(row) == 5]):
                    return False
                if not all([True for row in rewards if len(row) == 6]):
                    return False
                for reward in rewards:
                    if len(reward) != 6:
                        return False
                    if reward[0] not in [PromotionRewardTypes.AMOUNT_IN_MONEY.value,
                                         PromotionRewardTypes.FREE_SHIPPING.value,
                                         PromotionRewardTypes.FREE_PRODUCTS.value,
                                         PromotionRewardTypes.ACCESSORIES.value,
                                         PromotionRewardTypes.STORE_CREDIT.value]:
                        return False
                    if not all([True for r in reward[5] if len(r) == 5]):
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
                promotion_object.currency_id = currency_object.pk

                if promotion_type == "BUY":
                    promotion_object.promotion_type = PromotionTypes.BUY.value
                elif promotion_type == "RENT":
                    promotion_object.promotion_type = PromotionTypes.RENT.value
                elif promotion_type == "BUY":
                    promotion_object.promotion_type = PromotionTypes.ANY.value

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
                        is_new = product_rule[2]
                        print_type = product_rule[3]
                        min_qty_amount = product_rule[4]

                        product_rule_object = PromotionProductRule()
                        product_rule_object.product_id = product_id
                        product_rule_object.product_model = product_type
                        product_rule_object.is_new = is_new
                        product_rule_object.print_type = print_type
                        if by_amount_qty == "BY_AMOUNT":
                            product_rule_object.min_amount = min_qty_amount
                        elif by_amount_qty == "BY_QTY":
                            product_rule_object.min_qty = min_qty_amount

                        product_rule_object.save()

                        product_rule_objects += [product_rule_object]

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
                    gift_amount_in_percentage = reward[1]
                    gift_amount = reward[2]
                    store_credit = reward[3]
                    credit_expiry_datetime = reward[4]
                    products = reward[5]

                    reward_object = PromotionReward()
                    reward_object.reward_type = reward_type
                    if reward_type == PromotionRewardTypes.AMOUNT_IN_MONEY.value:
                        reward_object.gift_amount = gift_amount
                        if gift_amount_in_percentage:
                            reward_object.gift_amount_in_percentage = True
                        else:
                            reward_object.gift_amount_in_percentage = False
                    elif reward_type == PromotionRewardTypes.FREE_SHIPPING.value:
                        pass
                    elif reward_type == PromotionRewardTypes.FREE_PRODUCTS.value or reward_type == PromotionRewardTypes.ACCESSORIES.value:
                        reward_object.save()

                        promo_reward_product_instances = reward_object.products.all()
                        reward_object.products.clear()
                        promo_reward_product_instances.delete()

                        promo_reward_products = []
                        for reward_product_row in products:
                            pid = reward_product_row[0]
                            ptype = reward_product_row[1]
                            is_new = product_rule[2]
                            print_type = product_rule[3]
                            pquantity = reward_product_row[4]

                            promo_reward_product = PromotionRewardProduct()
                            promo_reward_product.product_id = pid
                            promo_reward_product.product_model = ptype
                            promo_reward_product.is_new = is_new
                            promo_reward_product.print_type = print_type
                            promo_reward_product.quantity = pquantity
                            promo_reward_product.save()

                            promo_reward_products += [promo_reward_product]

                        reward_object.products.add(*promo_reward_products)

                    elif reward_type == PromotionRewardTypes.STORE_CREDIT.value:
                        reward_object.store_credit = store_credit
                        reward_object.credit_expiry_time = credit_expiry_datetime

                    reward_object.save()

                    promo_rewards += [reward_object]

                promotion_object.rewards.add(*promo_rewards)
                
                return promotion_object
                
            except Exception as exp:
                print(str(exp))
                return False

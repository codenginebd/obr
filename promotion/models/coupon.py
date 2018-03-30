from datetime import datetime
from django.contrib.auth.models import User
from django.db import models, transaction
from enums import PromotionTypes, PromotionRewardTypes
from generics.models.base_entity import BaseEntity
from promotion.models.promotion_reward import PromotionReward
from promotion.models.promotion_reward_products import PromotionRewardProduct


class Coupon(BaseEntity):
    title = models.CharField(max_length=200)
    description = models.TextField(default='')
    coupon_code = models.CharField(max_length=200)
    coupon_type = models.IntegerField(default=PromotionTypes.BUY.value)
    start_date = models.DateField(null=True)
    expiry_date = models.DateField(null=True)
    referrer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    used_count = models.IntegerField(default=0)
    rewards = models.ManyToManyField(PromotionReward)

    @classmethod
    def find_the_best_coupon(cls, coupons, cart_total=None):
        best_coupon = None
        first_coupon = coupons.first()
        best_coupon_weight = 0
        for coupon in coupons:
            coupon_reward_weight = 0
            rewards = coupon.rewards.all()
            for reward in rewards:
                reward_weight = reward.get_reward_weight(cart_total=cart_total)
                if reward_weight:
                    coupon_reward_weight += reward_weight
            if coupon_reward_weight > best_coupon_weight:
                best_coupon_weight = coupon_reward_weight
                best_coupon = coupon
        if best_coupon:
            return coupons.filter(pk=best_coupon.pk)
        else:
            return coupons.filter(pk=first_coupon.pk)
    
    """
    coupon_code = "DHJGJHS"
    coupon_type = "BUY"
    cart_total = 500
    referrer_id = 200
    best = True

    Returns:
    
    {
        "coupon_code": "DHJGJHS",
        "coupon_instance": None,
        "amount": 0,
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
        'credit_expiry': None,
    }
                      
    """

    @classmethod
    def get_coupon_rewards(cls, coupon_code, coupon_type, cart_total, referrer_id=None, best=True, **kwargs):
        
        coupon_rewards = {
            "coupon_instance": None,
            "coupon_code": None,
            "coupon_type": coupon_type,
            "amount": 0,
            "free_shipping": False,
            "free_products": [],
            "accessories": [],
            "store_credit": 0,
            "credit_expiry": None,
            "currency_code": None,
        }        
        
        all_coupons = cls.get_coupons(coupon_code=coupon_code, coupon_type=coupon_type, referrer_id=referrer_id, **kwargs)
        if best:
            all_coupons = cls.find_the_best_coupon(coupons=all_coupons, cart_total=cart_total)
        if all_coupons is not None:
            all_reward_ids = []
            for coupon_instance in all_coupons:
                coupon_rewards["coupon_code"] = coupon_instance.coupon_code
                coupon_rewards["coupon_instance"] = coupon_instance
                all_reward_ids += coupon_instance.rewards.values_list('pk', flat=True)
                
            if all_reward_ids:
                all_rewards = PromotionReward.objects.filter(pk__in=all_reward_ids)
                for reward_instance in all_rewards:
                    if reward_instance.reward_type == PromotionRewardTypes.AMOUNT_IN_MONEY.value:
                        if reward_instance.gift_amount_in_percentage:
                            coupon_rewards["amount"] += reward_instance.gift_amount * cart_total
                        else:
                            coupon_rewards["amount"] += reward_instance.gift_amount
                    elif reward_instance.reward_type == PromotionRewardTypes.FREE_SHIPPING.value:
                        coupon_rewards["free_shipping"] = True
                    elif reward_instance.reward_type == PromotionRewardTypes.FREE_PRODUCTS.value:
                        for reward_product in reward_instance.products.all():
                            coupon_rewards["free_products"] += [
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
                            coupon_rewards["free_products"] += [
                                {
                                    "product_id": reward_product.product_id,
                                    "product_model": reward_product.product_model,
                                    "is_new": reward_product.is_new,
                                    "print_type": reward_product.print_type,
                                    "quantity": reward_product.quantity
                                }
                            ]
                    elif reward_instance.reward_type == PromotionRewardTypes.STORE_CREDIT.value:
                        coupon_rewards["store_credit"] += reward_instance.store_credit
                        coupon_rewards["credit_expiry"] = reward_instance.credit_expiry_time
                return coupon_rewards
            else:
                return None
            
        else:
            return None
    
    """
    coupon_code,
    coupon_type = "BUY"
    referrer_id
    """
    
    
    @classmethod
    def get_coupons(cls, coupon_code, coupon_type, referrer_id=None, **kwargs):
        todays_date = datetime.utcnow().date()
        if coupon_type not in [PromotionTypes.BUY.value, PromotionTypes.RENT.value, PromotionTypes.ANY.value]:
            return None
        all_coupons = cls.objects.filter(start_date__isnull=False,start_date__lte=todays_date,expiry_date__isnull=False,expiry_date__gte=todays_date, coupon_code=coupon_code, coupon_type=coupon_type)
        if referrer_id:
            all_coupons = all_coupons.filter(referrer_id=referrer_id)
        return all_coupons
    
    """
    title,
    description,
    coupon_code,
    coupon_type = PromotionTypes.BUY.value,
    start_date,
    expiry_date,
    referrer_id,
    rewards = [ ( REWARD_TYPE, gift_amount_in_percentage, GIFT_AMOUNT, store_credit, credit_expiry_time,
        products=[ ( ID, TYPE, is_new, print_type, quantity ) ] ) ]
    kwargs = { "pk": 1 }
    """
    
    
    @classmethod
    def create_or_update_coupon(cls, title, description, coupon_code, coupon_type, start_date, expiry_date, referrer_id=None, rewards=[], **kwargs):
        try:
            if coupon_type not in [PromotionTypes.BUY.value, PromotionTypes.RENT.value, PromotionTypes.ANY.value]:
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
            pk = kwargs.get("pk")
            if pk:
                coupon_objects = cls.objects.filter(pk=pk)
                if coupon_objects.exists():
                    coupon_object = coupon_objects.first()
                else:
                    return False
            else:
                coupon_object = cls()
            with transaction.atomic():
                coupon_object.title = title
                coupon_object.description = description
                coupon_object.coupon_code = coupon_code
                coupon_object.coupon_type = coupon_type
                coupon_object.start_date = start_date
                coupon_object.expiry_date = expiry_date
                if referrer_id:
                    coupon_object.referrer_id = referrer_id
                coupon_object.save()
                
                if pk:
                    if coupon_object.rewards.exists():
                        coupon_rewards = coupon_object.rewards.all()
                        coupon_object.rewards.clear()
                        coupon_rewards.delete()

                coupon_reward_list = []
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

                        coupon_reward_product_instances = reward_object.products.all()
                        reward_object.products.clear()
                        coupon_reward_product_instances.delete()

                        coupon_reward_products = []
                        for reward_product_row in products:
                            pid = reward_product_row[0]
                            ptype = reward_product_row[1]
                            is_new = reward_product_row[2]
                            print_type = reward_product_row[3]
                            pquantity = reward_product_row[4]

                            promo_reward_product = PromotionRewardProduct()
                            promo_reward_product.product_id = pid
                            promo_reward_product.product_model = ptype
                            promo_reward_product.is_new = is_new
                            promo_reward_product.print_type = print_type
                            promo_reward_product.quantity = pquantity
                            promo_reward_product.save()

                            coupon_reward_products += [promo_reward_product]

                        reward_object.products.add(*coupon_reward_products)

                    elif reward_type == PromotionRewardTypes.STORE_CREDIT.value:
                        reward_object.store_credit = store_credit
                        reward_object.credit_expiry_time = credit_expiry_datetime

                    reward_object.save()

                    coupon_reward_list += [reward_object]

                coupon_object.rewards.add(*coupon_reward_list)
                
                return coupon_object
                
        except Exception as exp:
            pass
        return None
    
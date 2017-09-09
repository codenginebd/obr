from django.db import models
from enums import PROMOTION_REWARD_TYPES
from generics.models.base_entity import BaseEntity
from promotion.models.ref_coupon_product import RefCouponProduct

"""
reward_type = 0 means amount in money(gift_amount), 1 means free shipping, 2 means free products(products),
3 means Accessories(accessories), 4 means store credit(store_credit)
"""


class PromotionReward(BaseEntity):
    reward_type = models.IntegerField(default=PROMOTION_REWARD_TYPES.AMOUNT_IN_MONEY)
    gift_amount = models.DecimalField(max_digits=20, decimal_places=2)
    store_credit = models.BooleanField(default=False)
    credit_expiry_time = models.IntegerField(default=0)
    products = models.ManyToManyField(RefCouponProduct)
    accessories = models.TextField(default='')
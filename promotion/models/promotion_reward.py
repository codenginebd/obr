from django.db import models
from enums import PromotionRewardTypes
from generics.models.base_entity import BaseEntity
from promotion.models.promotion_reward_products import PromotionRewardProduct

"""
reward_type = 0 means amount in money(gift_amount), 1 means free shipping, 2 means free products(products),
3 means Accessories(accessories), 4 means store credit(store_credit)
"""


class PromotionReward(BaseEntity):
    reward_type = models.IntegerField(default=PromotionRewardTypes.AMOUNT_IN_MONEY.value)
    gift_amount = models.DecimalField(max_digits=20, decimal_places=2)
    gift_amount_in_percentage = models.BooleanField(default=False)
    store_credit = models.BooleanField(default=False)
    credit_expiry_time = models.DateTimeField(null=True)
    products = models.ManyToManyField(PromotionRewardProduct)
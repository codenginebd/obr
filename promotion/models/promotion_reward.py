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

    def get_reward_weight(self, cart_total=None):
        if self.reward_type == PromotionRewardTypes.FREE_SHIPPING.value:
            return 20
        if self.reward_type == PromotionRewardTypes.AMOUNT_IN_MONEY.value:
            if not self.gift_amount_in_percentage:
                if self.gift_amount > 150:
                    return 21
                else:
                    return 19
            else:
                if cart_total:
                    gift_amount = self.gift_amount * cart_total
                    if gift_amount > 150:
                        return 21
                    else:
                        return 19
                else:
                    return 19
        if self.reward_type == PromotionRewardTypes.FREE_PRODUCTS.value:
            return 18
        if self.reward_type == PromotionRewardTypes.ACCESSORIES.value:
            return 17
        if self.reward_type == PromotionRewardTypes.STORE_CREDIT.value:
            if self.store_credit > 200:
                return 22
            else:
                return 16

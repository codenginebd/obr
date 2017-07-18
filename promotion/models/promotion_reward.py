from django.db import models
from generics.models.base_entity import BaseEntity


class PromotionReward(BaseEntity):
    reward_type = models.IntegerField(default=0) # 0 means money amount, 1 means free shipping, 2 means free books, 3 means other gift item
    product_id = models.BigIntegerField(null=True)
    product_model = models.CharField(max_length=200, null=True)
    gift_amount = models.DecimalField(max_digits=20, decimal_places=2)
    store_credit = models.BooleanField(default=False)
    credit_expiry_time = models.IntegerField(default=0)
    books_total = models.IntegerField(default=1)
    accessories = models.TextField(default='')
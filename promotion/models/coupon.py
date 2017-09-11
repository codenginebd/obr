from django.contrib.auth.models import User
from django.db import models
from enums import PROMOTION_TYPES
from generics.models.base_entity import BaseEntity
from promotion.models.promotion_reward import PromotionReward


class Coupon(BaseEntity):
    coupon_code = models.CharField(max_length=200)
    coupon_type = models.IntegerField(default=PROMOTION_TYPES.BUY.value)
    start_date = models.DateField(null=True)
    expiry_date = models.DateField(null=True)
    referrer = models.ForeignKey(User, null=True)
    used_count = models.IntegerField(default=0)
    rewards = models.ManyToManyField(PromotionReward)
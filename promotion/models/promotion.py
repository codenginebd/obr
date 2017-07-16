from django.db import models
from generics.models.base_entity import BaseEntity
from promotion.models.promotion_reward import PromotionReward
from promotion.models.promotion_rule import PromotionRule


class Promotion(BaseEntity):
    title = models.CharField(max_length=200)
    description = models.TextField(default='')
    rules = models.ManyToManyField(PromotionRule)
    rewards = models.ManyToManyField(PromotionReward)
from django.db import models
from generics.models.base_entity import BaseEntity


class PromotionRewardProduct(BaseEntity):
    product_id = models.BigIntegerField(null=True)
    product_model = models.CharField(max_length=200, null=True)
    is_new = models.BooleanField(default=True)
    print_type = models.CharField(max_length=100, null=True)
    quantity = models.IntegerField(default=1)
from django.db import models
from generics.models.base_entity import BaseEntity


class PromotionProductRule(BaseEntity):
    product_id = models.BigIntegerField(null=True)
    product_model = models.CharField(max_length=200, null=True)
    is_new = models.BooleanField(default=True)
    print_type = models.CharField(max_length=100, null=True)
    min_qty = models.IntegerField(default=0)
    min_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
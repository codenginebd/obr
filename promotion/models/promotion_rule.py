from django.db import models
from generics.models.base_entity import BaseEntity


class PromotionRule(BaseEntity):
    product_id = models.BigIntegerField(null=True)
    product_model = models.CharField(max_length=200, null=True)
    min_qty = models.IntegerField(default=0)
    min_amount = models.DecimalField(max_digits=20, decimal_places=2)
    by_qty = models.BooleanField(null=False)
    by_amount = models.BooleanField(null=False)
    by_books = models.BooleanField(null=False)
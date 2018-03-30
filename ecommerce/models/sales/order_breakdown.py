from django.db import models
from generics.models.base_entity import BaseEntity
from promotion.models.promotion import Promotion


class OrderBreakdown(BaseEntity):
    order_type = models.IntegerField(default=0)  # 1 for Sale, 0 for Rent
    quantity = models.IntegerField(default=0)
    initial_payable_rent_price = models.DecimalField(max_digits=20, decimal_places=2)
    rent_price = models.DecimalField(max_digits=20, decimal_places=2) # This is the percentage of initial_payable_rent_price field.
    coupon_applied = models.BooleanField(default=False)
    coupon_code = models.CharField(max_length=100, blank=True, null=True)
    promotion_applied = models.BooleanField(default=False)
    promotion = models.ForeignKey(Promotion, null=True, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        abstract = True
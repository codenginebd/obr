from django.db import models
from generics.models.base_entity import BaseEntity
from generics.models.sales.rent_plan import RentPlan


class PriceMatrix(BaseEntity):
    plan = models.ForeignKey(RentPlan, null=True)
    is_rent = models.BooleanField(default=False)
    offer_price_p = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # value in percentage
    offer_price_v = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # value in value
    special_price = models.BooleanField(default=False)
    offer_date_start = models.BigIntegerField(default=0)
    offer_date_end = models.BigIntegerField(default=0)
    product_id = models.BigIntegerField(null=False)
    product_model = models.CharField(max_length=100)
    is_new = models.IntegerField(default=0)
    print_type = models.CharField(max_length=50)  # COL, ORI, ECO
    base_price = models.DecimalField(max_digits=20, decimal_places=2)
    market_price = models.DecimalField(max_digits=20, decimal_places=2)

from django.db import models
from ecommerce.models.rent_plan import RentPlan
from ecommerce.models.sales.rent_plan_relation import RentPlanRelation
from generics.models.base_entity import BaseEntity
from payment.models.currency import Currency


class PriceMatrix(BaseEntity):
    rent_plans = models.ManyToManyField(RentPlan, through=RentPlanRelation)
    is_rent = models.BooleanField(default=False)
    offer_price_p = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # value in percentage
    offer_price_v = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # value in value
    special_price = models.BooleanField(default=False)
    offer_date_start = models.BigIntegerField(default=0)
    offer_date_end = models.BigIntegerField(default=0)
    product_code = models.CharField(max_length=20)
    product_model = models.CharField(max_length=100)
    is_new = models.IntegerField(default=0)
    print_type = models.CharField(max_length=50)  # COL, ORI, ECO
    base_price = models.DecimalField(max_digits=20, decimal_places=2)
    market_price = models.DecimalField(max_digits=20, decimal_places=2)
    sale_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    currency = models.ForeignKey(Currency)
    
    class Meta:
        index_together = [ 'product_code', 'product_model', 'is_new', 'print_type' ]
from django.db import models
from generics.models.base_entity import BaseEntity
from generics.models.sales.rent_plan import RentPlan


class PriceConfig(BaseEntity):
    plan = models.ForeignKey(RentPlan, null=True)
    is_rent = models.BooleanField(default=False)
    value_p = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # value in percentage
    value_v = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # value in value
    special_price = models.BooleanField(default=False)

    class Meta:
        abstract = True

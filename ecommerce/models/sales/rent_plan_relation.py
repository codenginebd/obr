from django.db import models
from ecommerce.models.rent_plan import RentPlan
from generics.models.base_entity import BaseEntity


class RentPlanRelation(BaseEntity):
    plan = models.ForeignKey(RentPlan)
    price_matrix = models.ForeignKey('PriceMatrix')
    start_time = models.BigIntegerField(default=0)
    end_time = models.BigIntegerField(default=0)
    is_special_offer = models.BooleanField(default=False)
    special_rate = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)
    
from django.db import models
from generics.models.base_entity import BaseEntity
from generics.models.sales.price_matrix import PriceMatrix
from generics.models.sales.rent_plan import RentPlan


class RentPlanRelation(BaseEntity):
    plan = models.ForeignKey(RentPlan)
    price_matrix = models.ForeignKey(PriceMatrix)
    start_time = models.BigIntegerField(default=0)
    end_time = models.BigIntegerField(default=0)
    
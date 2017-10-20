from django.db import models
from datetime import datetime

from django.db.models.query_utils import Q

from ecommerce.models.rent_plan import RentPlan
from generics.models.base_entity import BaseEntity
from engine.clock.Clock import Clock


class RentPlanRelationManager(models.Manager):
    def get_queryset(self):
        queryset = super(RentPlanRelationManager, self).get_queryset()
        now_datetime = datetime.now()
        now_ts = Clock.convert_datetime_to_utc_timestamp(now_datetime)
        # queryset = queryset.filter(Q(is_special_offer=False) | ( Q(is_special_offer=True) & Q(start_time__lte=now_ts) & Q(end_time__lte=now_ts)))
        return queryset


class RentPlanRelation(BaseEntity):
    plan = models.ForeignKey(RentPlan)
    price_matrix = models.ForeignKey('PriceMatrix')
    start_time = models.BigIntegerField(null=True)
    end_time = models.BigIntegerField(null=True)
    is_special_offer = models.BooleanField(default=False)
    special_rate = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)
    rent_rate = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)
    
    
    objects = RentPlanRelationManager()
    
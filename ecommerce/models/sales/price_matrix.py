from django.db import models
from datetime import datetime
from ecommerce.models.rent_plan import RentPlan
from ecommerce.models.sales.rent_plan_relation import RentPlanRelation
from generics.models.base_entity import BaseEntity
from payment.models.currency import Currency
from engine.clock.Clock import Clock

class PriceMatrixManager(models.Manager):
    def get_queryset(self):    
        todays_datetime = datetime.now()
        todays_ts = Clock.convert_datetime_to_utc_timestamp(todays_datetime)    
        queryset = super(PriceMatrixManager, self).get_queryset()
        queryset = queryset.filter(Q(is_rent=False) | (Q(is_rent=True) & Q(offer_date_start__isnull=False) & Q(offer_date_start__lte=todays_ts) & Q(offer_date_end__isnull=False) & Q(offer_date_end__gte=todays_ts)))
        return queryset

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
    
    objects = PriceMatrixManager()
    
    class Meta:
        index_together = [ 'product_code', 'product_model', 'is_new', 'print_type' ]
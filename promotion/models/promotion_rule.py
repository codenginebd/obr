from django.db import models
from generics.models.base_entity import BaseEntity


class PromotionRule(BaseEntity):
    product_id = models.BigIntegerField(null=True)
    product_model = models.CharField(max_length=200, null=True)
    min_qty = models.IntegerField(default=0)
    min_amount = models.DecimalField(max_digits=20, decimal_places=2)
    by_qty = models.BooleanField(null=False)
    by_amount = models.BooleanField(null=False)
    by_products = models.BooleanField(null=False)
    start_date = models.BigIntegerField(default=0)
    end_date = models.BigIntegerField(default=0)

    @classmethod
    def create_or_update_promotion_rule(cls, pk=None, product_id=None, product_model=None,
                                        min_qty = None, min_amount=None,by_qty=None, by_amount=None,
                                        by_products=None,start_date=None,end_date=None):

        if by_qty:
            if any([not min_qty, not product_id, not product_model, not start_date, not end_date]):
                return False
        elif by_amount:
            if any([not min_qty, not product_id, not product_model, not start_date, not end_date]):
                return False

        return False
from django.db import models
from generics.models.base_entity import BaseEntity

class WishList(BaseEntity):
    product_id = models.BigIntegerField()
    product_model = models.CharField(max_lenth=200)
    is_new = models.BooleanField(default=True)
    print_type = models.CharField(max_length=20)
    qty = models.IntegerField(default=0)
    notify = models.BooleanField(default=False)
from django.db import models
from generics.models.base_entity import BaseEntity


class FrontListProduct(BaseEntity):
    product_id = models.BigIntegerField()
    product_model = models.CharField(max_length=100)
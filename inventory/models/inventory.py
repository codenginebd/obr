from django.db import models
from generics.models.base_entity import BaseEntity


class Inventory(BaseEntity):
    stock = models.BigIntegerField(default=0)
    
    class Meta:
        abstract = True
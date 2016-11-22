from django.db import models
from generics.models.base_entity import BaseEntity


class RentPlan(BaseEntity):
    name = models.CharField(max_length=200)
    days = models.IntegerField(default=1)
from django.db import models

from generics.models.base_entity import BaseEntity


class DeliveryAgent(BaseEntity):
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    #is_active = models.BooleanField(default=True)
from django.db import models
from generics.models.base_entity import BaseEntity


class LocationEntity(BaseEntity):
    type = models.CharField(max_length=300)
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
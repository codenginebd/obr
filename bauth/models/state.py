from django.db import models

from bauth.models.country import Country
from generics.models.base_entity import BaseEntity


class State(BaseEntity):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200, blank=True)
    parent = models.ForeignKey(Country)
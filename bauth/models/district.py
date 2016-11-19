from django.db import models
from bauth.models.state import State
from generics.models.base_entity import BaseEntity


class District(BaseEntity):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200, blank=True)
    parent = models.ForeignKey(State)
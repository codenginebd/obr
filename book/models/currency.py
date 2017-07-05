from django.db import models

from bauth.models.country import Country
from generics.models.base_entity import BaseEntity


class Currency(BaseEntity):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=10)
    country = models.ForeignKey(Country, null=True)
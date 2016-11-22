from django.db import models

from generics.models.base_entity import BaseEntity


class Currency(BaseEntity):
    name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=10)
from django.db import models
from generics.models.base_entity import BaseEntity


class FrontPalette(BaseEntity):
    name = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
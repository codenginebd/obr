from django.db import models
from bauth.models.district import District
from generics.models.base_entity import BaseEntity


class Upazila(BaseEntity):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200, blank=True)
    parent = models.ForeignKey(District)
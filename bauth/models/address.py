from django.db import models
from bauth.models.country import Country
from bauth.models.district import District
from bauth.models.state import State
from bauth.models.upazila import Upazila
from generics.models.base_entity import BaseEntity


class Adress(BaseEntity):
    type = models.CharField(max_length=20)
    street1 = models.CharField(max_length=500)
    street2 = models.CharField(max_length=500, blank=True)
    upazila = models.ForeignKey(Upazila, null=True, related_name='+')
    district = models.ForeignKey(District, null=True, related_name='+')
    state = models.ForeignKey(State, null=True, related_name='+')
    country = models.ForeignKey(Country, null=True, related_name='+')
from django.db import models
from bauth.models.country import Country
from bauth.models.district import District
from bauth.models.state import State
from bauth.models.upazila import Upazila
from generics.models.base_entity import BaseEntity


class Address(BaseEntity):
    type = models.CharField(max_length=20)
    street1 = models.CharField(max_length=500)
    street2 = models.CharField(max_length=500, blank=True)
    upazila = models.ForeignKey(Upazila, null=True, related_name='+', on_delete=models.CASCADE)
    district = models.ForeignKey(District, null=True, related_name='+', on_delete=models.CASCADE)
    state = models.ForeignKey(State, null=True, related_name='+', on_delete=models.CASCADE)
    country = models.ForeignKey(Country, null=True, related_name='+', on_delete=models.CASCADE)
    nearest_landmark = models.CharField(max_length=500, blank=True, null=True)
    verified = models.BooleanField(default=False)

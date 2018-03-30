from django.contrib.auth.models import User
from django.db import models

from bauth.models.address import Address
from generics.models.base_entity import BaseEntity


class BUser(BaseEntity):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, blank=True)
    is_verified = models.BooleanField(default=False)
    social_signup = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, blank=True)
    addresses = models.ManyToManyField(Address)

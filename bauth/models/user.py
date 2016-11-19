from django.contrib.auth.models import User
from django.db import models

from bauth.models.address import Adress
from generics.models.base_entity import BaseEntity


class BUser(BaseEntity):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=200, blank=True)
    social_signup = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, blank=True)
    addresses = models.ManyToManyField(Adress)
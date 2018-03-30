from django.contrib.auth.models import User
from django.db import models
from generics.models.base_entity import BaseEntity


class Referral(BaseEntity):
    referral_code = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    referred_count = models.BigIntegerField(default=0)
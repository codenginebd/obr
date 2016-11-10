from django.contrib.auth.models import User
from django.db import models

class BUser(models.Model):
    user = models.OneToOneField(User)
    middle_name = models.CharField(max_length=200, blank=True)
    phone_
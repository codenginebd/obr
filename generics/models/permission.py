from django.db import models
from generics.models.base_entity import BaseEntity


class BRPermission(BaseEntity):
    value = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
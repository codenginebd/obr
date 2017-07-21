from django.db import models
from generics.models.base_entity import BaseEntity


class Phone(BaseEntity):
    is_primary = models.BooleanField(default=False)
    number = models.CharField(max_length=255, null=False, blank=False)
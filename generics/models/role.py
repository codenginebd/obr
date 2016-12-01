from django.db import models
from generics.models.base_entity import BaseEntity


class BRole(BaseEntity):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True)

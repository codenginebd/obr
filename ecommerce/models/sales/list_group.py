from django.db import models
from generics.models.base_entity import BaseEntity


class ListGroup(BaseEntity):
    name = models.CharField(max_length=500)
    name_2 = models.CharField(max_length=500, blank=True)
    show_2 = models.BooleanField(default=False)
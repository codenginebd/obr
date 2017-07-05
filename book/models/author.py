from django.db import models

from generics.models.base_entity import BaseEntity


class Author(BaseEntity):
    name = models.CharField(max_length=255, blank = True)
    description = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True)
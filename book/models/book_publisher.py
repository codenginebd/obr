from django.db import models

from generics.models.base_entity import BaseEntity


class BookPublisher(BaseEntity):
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True)
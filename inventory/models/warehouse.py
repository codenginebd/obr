from django.db import models

from generics.models.base_entity import BaseEntity


class BookWarehouse(BaseEntity):
    name = models.CharField(max_length=500)
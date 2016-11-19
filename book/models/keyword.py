from django.db import models

from generics.models.base_entity import BaseEntity


class TagKeyword(BaseEntity):
    name = models.CharField(max_length=100)
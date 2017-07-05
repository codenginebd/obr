from django.db import models

from generics.models.base_entity import BaseEntity


class Email(BaseEntity):
    name = models.EmailField(max_length=500)
    is_primary = models.BooleanField(default=False)
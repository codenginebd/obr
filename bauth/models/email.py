from django.db import models
from generics.models.base_entity import BaseEntity


class Email(BaseEntity):
    is_primary = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, null=False, blank=False)
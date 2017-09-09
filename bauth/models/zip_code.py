from django.db import models
from generics.models.base_entity import BaseEntity


class ZipCode(BaseEntity):
    zip_code = models.CharField(max_length=100)
from django.db import models
from generics.models.base_entity import BaseEntity


class BookLanguage(BaseEntity):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=10)
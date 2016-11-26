from django.db import models

from generics.models.base_entity import BaseEntity


class ErrorLog(BaseEntity):
    url = models.CharField(max_length=500)
    stacktrace = models.TextField()

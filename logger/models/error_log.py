from django.db import models

from generics.models.base_entity import BaseEntity


class ErrorLog(BaseEntity):
    url = models.CharField(max_length=500)
    stacktrace = models.TextField(blank=True, null=True)
    
    @classmethod
    def log(cls, url, stacktrace=None):
        instance = cls()
        instance.url = url
        if stacktrace:
            instance.stacktrace = stacktrace
        instance.save()

from django.db import models

from generics.models.base_entity import BaseEntity


class ErrorLog(BaseEntity):
    context = models.CharField(max_length=200, blank=True)
    url = models.CharField(max_length=500)
    stacktrace = models.TextField(blank=True, null=True)
    
    @classmethod
    def log(cls, url, stacktrace=None, context=None):
        instance = cls()
        if context:
            instance.context = context
        instance.url = url
        if stacktrace:
            instance.stacktrace = stacktrace
        instance.save()

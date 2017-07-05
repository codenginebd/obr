from django.db import models
from generics.models.base_entity import BaseEntity


class EmailLog(BaseEntity):
    sender = models.CharField(max_length=500)
    receiver = models.CharField(max_length=500)
    subject = models.CharField(max_length=500)
    html_body = models.TextField(blank=True, null=True)
    text_body = models.TextField(blank=True, null=True)
    job_id = models.CharField(max_length=500)
    status = models.CharField(max_length=20,blank=True)  # SUCCESS, FAILED
    exception_stacktrace = models.TextField(blank=True)

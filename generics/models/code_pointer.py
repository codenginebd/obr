from django.db import models


class CodePointer(models.Model):
    model_name = models.CharField(max_length=500)
    value = models.BigIntegerField(default=0)
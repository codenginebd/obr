from django.db import models

from generics.models.base_entity import BaseEntity


class BookUploadHistory(BaseEntity):
    file_name = models.CharField(max_length=500)
    total_count = models.IntegerField(default=0)
    new_uploaded = models.IntegerField(default=0)
    sheet = models.CharField(max_length=500)
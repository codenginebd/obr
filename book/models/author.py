from django.db import models
from book_rental.models.base_entity import BaseEntity


class Author(BaseEntity):
    first_name = models.CharField(max_length=255, blank = True)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True)
from django.db import models
from book_rental.models.base_entity import BaseEntity

class BookCategory(BaseEntity):
    name = models.CharField(max_length=500)
    parent = models.ForeignKey('self', null=True)
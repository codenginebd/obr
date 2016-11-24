from django.db import models

from book.models.category import BookCategory
from generics.models.base_entity import BaseEntity


class Book(BaseEntity):
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    category = models.ForeignKey(BookCategory, null=True)
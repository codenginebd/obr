from django.db import models

from book.models.book_edition import BookEdition
from generics.models.base_entity import BaseEntity


class Inventory(BaseEntity):
    book = models.ForeignKey(BookEdition)
    stock = models.BigIntegerField(default=0)
    
    class Meta:
        abstract = True
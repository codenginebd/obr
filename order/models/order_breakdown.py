from django.db import models

from book.models.book_edition import BookEdition
from book_rental.models.base_entity import BaseEntity

class BookOrderBreakdown(BaseEntity):
    book = models.ForeignKey(BookEdition)
    order_type = models.IntegerField(default=0) #1 for Sale, 0 for Rent
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
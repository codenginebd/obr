from django.db import models

from book.models.book_edition import BookEdition
from generics.models.base_entity import BaseEntity


class PromotionRule(BaseEntity):
    book = models.ForeignKey(BookEdition)
    min_qty = models.IntegerField(default=0)
    min_amount = models.DecimalField(max_digits=20, decimal_places=2)
    by_qty = models.BooleanField(null=False)
    by_amount = models.BooleanField(null=False)
    by_books = models.BooleanField(null=False)
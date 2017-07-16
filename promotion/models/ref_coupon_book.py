from django.db import models

from book.models.book_edition import BookEdition
from generics.models.base_entity import BaseEntity


class RefCouponBook(BaseEntity):
    book = models.ForeignKey(BookEdition)
    quantity = models.IntegerField(default=1)
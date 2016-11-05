from django.db import models
from book.models.book_edition import BookEdition
from book_rental.models.base_entity import BaseEntity

class BookInventory(BaseEntity):
    book = models.ForeignKey(BookEdition)
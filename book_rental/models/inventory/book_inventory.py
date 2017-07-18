from django.db import models

from book_rental.models.sales.book import Book
from inventory.models.inventory import Inventory


class BookInventory(Inventory):
    book = models.ForeignKey(Book)
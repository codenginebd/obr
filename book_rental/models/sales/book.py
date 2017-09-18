from django.db import models

from book_rental.models.author import Author
from book_rental.models.book_publisher import BookPublisher
from book_rental.models.language import BookLanguage
from ecommerce.models.sales.product import Product


class Book(Product):
    isbn = models.CharField(max_length=500, blank=True)  # The 10 digit ISBN code
    isbn13 = models.CharField(max_length=500, blank=True)
    edition = models.CharField(max_length=100)
    publisher = models.ForeignKey(BookPublisher, null=True)
    authors = models.ManyToManyField(Author)
    publish_date = models.DateField(null=True)
    language = models.ForeignKey(BookLanguage)
    page_count = models.IntegerField(default=0)
from django.db import models
from book.models.author import Author
from book.models.book import Book
from book.models.book_publisher import BookPublisher
from book.models.keyword import TagKeyword
from book.models.price_currency import PriceCurrency
from generics.models.base_entity import BaseEntity


class BookEdition(BaseEntity):
    isbn = models.CharField(max_length=500, blank=True)
    book = models.ForeignKey(Book)
    edition = models.CharField(max_length=100)
    publisher = models.ForeignKey(BookPublisher, null=True)
    authors = models.ManyToManyField(Author)
    publish_date = models.DateField(null=True)
    tags = models.ManyToManyField(TagKeyword)
    language = models.CharField(max_length=100, blank=True)
    page_count = models.IntegerField(default=0)
    is_used = models.BooleanField(default=False)
    base_prices = models.ManyToManyField(PriceCurrency)
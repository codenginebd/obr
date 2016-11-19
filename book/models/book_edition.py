from django.db import models

from book.models.author import Author
from book.models.book import Book
from book.models.book_publisher import BookPublisher
from book.models.keyword import TagKeyword
from generics.models.base_entity import BaseEntity

class BookEdition(BaseEntity):
    isbn = models.CharField(max_length=500, blank=True)
    book = models.ForeignKey(Book)
    edition = models.CharField(max_length=100)
    publisher = models.ForeignKey(BookPublisher, null=True)
    authors = models.ManyToMany(Author)
    publish_date = models.DateField(null=True)
    tags = models.ManyToMany(TagKeyword)
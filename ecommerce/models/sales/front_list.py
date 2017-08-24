from django.db import models

from book_rental.models.sales.book import Book
from ecommerce.models.sales.list_group import ListGroup
from generics.models.base_entity import BaseEntity


class FrontList(BaseEntity):
    name = models.CharField(max_length=500)
    name_2 = models.CharField(max_length=500, blank=True)
    show_name_2 = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    description_2 = models.TextField(blank=True)
    show_description_2 = models.BooleanField(default=False)
    detail_url = models.CharField(max_length=200, blank=True)
    group = models.ForeignKey(ListGroup)
    items = models.ManyToManyField(Book)
from django.db import models

from book_rental.models.sales.book_order_breakdown import BookOrderBreakdown
from ecommerce.models.sales.order import Order


class BookOrder(Order):
    breakdown = models.ManyToManyField(BookOrderBreakdown)
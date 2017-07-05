from django.db import models

from book.models.book_edition import BookEdition
from book.models.rent_plan import RentPlan
from generics.models.base_entity import BaseEntity


class PriceConfig(BaseEntity):
    book_edition = models.ForeignKey(BookEdition)
    plan = models.ForeignKey(RentPlan)
    value_p = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # value in percentage
    value_v = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # value in value
    special_price = models.BooleanField(default=False)

    class Meta:
        abstract = True

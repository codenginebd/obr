from django.db import models

from book.models.currency import Currency
from generics.models.base_entity import BaseEntity


class PriceCurrency(BaseEntity):
    currency = models.ForeignKey(Currency)
    base_price = models.DecimalField(decimal_places=2, max_digits=20)
    initial_payable_rent = models.DecimalField(decimal_places=2, max_digits=20)
    initial_payable_buy = models.DecimalField(decimal_places=2, max_digits=20)
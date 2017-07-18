from django.db import models
from generics.models.base_entity import BaseEntity
from generics.models.sales.currency import Currency


class PriceCurrency(BaseEntity):
    currency = models.ForeignKey(Currency)
    base_price = models.DecimalField(decimal_places=2, max_digits=20)
    initial_payable_rent = models.DecimalField(decimal_places=2, max_digits=20)
    initial_payable_buy = models.DecimalField(decimal_places=2, max_digits=20)
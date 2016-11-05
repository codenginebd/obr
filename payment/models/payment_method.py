from django.db import models
from book_rental.models.base_entity import BaseEntity

class PaymentMethod(BaseEntity):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
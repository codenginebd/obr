from django.db import models
from book_rental.models.base_entity import BaseEntity

class BookWarehouse(BaseEntity):
    name = models.CharField(max_length=500)
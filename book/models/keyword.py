from django.db import models
from book_rental.models.base_entity import BaseEntity

class TagKeyword(BaseEntity):
    name = models.CharField(max_length=100)
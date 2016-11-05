from django.db import models
from django.auth.models import User
from book_rental.models.base_entity import BaseEntity

class ClientUser(BaseEntity):
    user = models.OneToOne(User)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=200)
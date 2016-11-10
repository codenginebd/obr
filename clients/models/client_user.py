from django.contrib.auth.models import User
from django.db import models
from book_rental.models.base_entity import BaseEntity
from clients.models.email import Email
from clients.models.phone_number import PhoneNumber


class ClientUser(BaseEntity):
    user = models.OneToOne(User)
    last_name = models.CharField(max_length=100)
    email_addresses = models.ManyToManyField(Email)
    phones = models.ManyToManyField(PhoneNumber)
    gender = models.CharField(max_length=200, blank=True)
    birth_date = models.DateField(null=True)
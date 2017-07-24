from django.conf import settings
from django.db import models

from bauth.models.address import Address
from bauth.models.email import Email
from bauth.models.phone import Phone
from generics.models.base_entity import BaseEntity


class BookPublisher(BaseEntity):
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    address = models.ForeignKey(Address, null=True)
    phones = models.ManyToManyField(Phone)
    emails = models.ManyToManyField(Email)
    image = models.ImageField(max_length=500, upload_to='publisher/', null=True)
    thumbnail = models.ImageField(max_length=500, upload_to='publisher/thumbnails/', null=True)
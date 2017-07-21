from django.conf import settings
from django.db import models

from bauth.models.address import Address
from bauth.models.email import Email
from bauth.models.phone import Phone
from generics.models.base_entity import BaseEntity


class Author(BaseEntity):
    name = models.CharField(max_length=255, blank = True)
    description = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True)
    address = models.ForeignKey(Address, null=True)
    phones = models.ManyToManyField(Phone)
    emails = models.ManyToManyField(Email)
    image = models.ImageField(max_length=500, upload_to=settings.MEDIA_AUTHOR_PATH, null=True)
    thumbnail = models.ImageField(max_length=500, upload_to=settings.MEDIA_AUTHOR_THUMB_PATH, null=True)

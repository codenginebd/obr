from django.conf import settings
from django.db import models

from bauth.models.address import Address
from bauth.models.email import Email
from bauth.models.phone import Phone
from generics.mixin.thumbnail_model_mixin import ThumbnailModelMixin
from generics.models.base_entity import BaseEntity


class Author(BaseEntity, ThumbnailModelMixin):
    name = models.CharField(max_length=255, blank = True)
    description = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True)
    address = models.ForeignKey(Address, null=True)
    phones = models.ManyToManyField(Phone)
    rating = models.FloatField(default=0)
    emails = models.ManyToManyField(Email)
    image = models.ImageField(max_length=500, upload_to='author/', null=True)
    thumbnail = models.ImageField(max_length=500, upload_to='author/thumbnails/', null=True)
    nationalities = models.ManyToManyField(Country)
    languages = models.ManyToManyField(Language)

    def save(self):
        try:
            self.create_thumbnail()
            # self.save()
        except Exception as msg:
            print("Thumbnail creation failed.")
        super(Author, self).save()

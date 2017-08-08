from django.conf import settings
from django.db import models

from bauth.models.address import Address
from bauth.models.email import Email
from bauth.models.phone import Phone
from generics.mixin.thumbnail_model_mixin import ThumbnailModelMixin
from generics.models.base_entity import BaseEntity


class BookPublisher(BaseEntity, ThumbnailModelMixin):
    name = models.CharField(max_length=500)
    name_2 = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    description_2 = models.TextField(blank=True)
    show_2 = models.BooleanField(default=False)
    address = models.ForeignKey(Address, null=True)
    phones = models.ManyToManyField(Phone)
    emails = models.ManyToManyField(Email)
    image = models.ImageField(max_length=500, upload_to='publisher/', null=True)
    thumbnail = models.ImageField(max_length=500, upload_to='publisher/thumbnails/', null=True)

    def save(self):
        try:
            self.create_thumbnail()
            # self.save()
        except Exception as msg:
            print("Thumbnail creation failed.")
        super(BookPublisher, self).save()
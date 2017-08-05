from django.db import models
from generics.mixin.thumbnail_model_mixin import ThumbnailModelMixin
from generics.models.base_entity import BaseEntity


class ProductImage(BaseEntity, ThumbnailModelMixin):
    image = models.ImageField(max_length=500, upload_to='books/', null=True)
    thumbnail = models.ImageField(max_length=500, upload_to='books/thumbnails/', null=True)

    def save(self):
        try:
            self.create_thumbnail()
        except Exception as msg:
            print("Thumbnail creation failed.")
        super(ProductImage, self).save()
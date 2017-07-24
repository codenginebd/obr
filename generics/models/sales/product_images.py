from django.db import models
from generics.models.base_entity import BaseEntity
from generics.models.sales.product import Product


class ProductImage(BaseEntity):
    product = models.ForeignKey(Product)
    image = models.ImageField(max_length=500, upload_to='books/', null=True)
    thumbnail = models.ImageField(max_length=500, upload_to='books/thumbnails/', null=True)
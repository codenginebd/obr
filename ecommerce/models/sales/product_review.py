from django.contrib.auth.models import User
from django.db import models
from generics.models.base_entity import BaseEntity


class ProductReview(BaseEntity):
    product_model = models.CharField(max_length=250)
    product_id = models.BigIntegerField()
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    review_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    review_by_name = models.CharField(max_length=500)
    rating_value = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    comment = models.TextField(null=True, blank=True)

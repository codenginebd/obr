from django.contrib.auth.models import User
from django.db import models
from generics.models.base_entity import BaseEntity
from promotion.models.ref_coupon_product import RefCouponProduct


class RefCoupon(BaseEntity):
    coupon_code = models.CharField(max_length=200)
    start_time = models.BigIntegerField(default=0)
    expiry_time = models.IntegerField(default=0)
    referrer = models.ForeignKey(User)
    used_count = models.IntegerField(default=0)
    gift_type = models.IntegerField(default=0) # 0 amount, 1 book_rental, 2 free shipping
    gift_amount = models.DecimalField(max_digits=20, decimal_places=2)
    books = models.ManyToManyField(RefCouponProduct)
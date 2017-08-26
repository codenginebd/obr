from django.contrib.auth.models import User
from django.db import models
from django.db.models.aggregates import Sum
from book_rental.models.sales.book import Book
from generics.models.base_entity import BaseEntity


class ProductRating(BaseEntity):
    product_model = models.CharField(max_length=250)
    product_id = models.BigIntegerField()
    rating_by = models.ForeignKey(User, null=True)
    rated_by_name = models.CharField(max_length=500)
    rating_value = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(ProductRating, self).save(force_insert=force_insert, force_update=force_update, using=using,
             update_fields=update_fields)
        try:
            if self.product_model == Book.__name__:
                book_objects = Book.objects.filter(pk=self.product_id)
                if book_objects.exists():
                    book_object = book_objects.first()
                    rating_objects = self.__class__.objects.filter(product_model=self.product_model,
                                                  product_id=self.product_id).aggregate(total_rating=Sum('rating_value'))
                    if rating_objects.exists():
                        rating_object = rating_objects.first()
                        book_object.rating = rating_object.total_rating
                        book_object.save()
        except Exception as exp:
            pass

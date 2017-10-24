from django.db import models
from generics.models.base_entity import BaseEntity


class PromotionRewardProduct(BaseEntity):
    product_id = models.BigIntegerField(null=True)
    product_model = models.CharField(max_length=200, null=True)
    is_new = models.BooleanField(default=True)
    print_type = models.CharField(max_length=100, null=True)
    quantity = models.IntegerField(default=1)
    
    def get_product_instance(self):
        if self.product_model == "Book":
            Book = load_model(app_label="book_rental", model_name="Book")
            return Book.objects.get(pk=self.product_id)
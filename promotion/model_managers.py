from django.db import models


class PromotionManagerByQuantity(models.Manager):
    
    def get_queryset(self):
        promo_ids = super(PromotionManagerByQuantity, self).get_queryset().filter(rules__by_qty=True,rules__by_amount=False,rules__by_products=False).values_list('pk', flat=True)
        return self.__class__.objects.filter(pk__in=promo_ids)
        
        
class PromotionManagerByAmount(models.Manager):
    
    def get_queryset(self):
        promo_ids = super(PromotionManagerByQuantity, self).get_queryset().filter(rules__by_qty=False,rules__by_amount=True,rules__by_products=False).values_list('pk', flat=True)
        return self.__class__.objects.filter(pk__in=promo_ids)
        
        
class PromotionManagerByProducts(models.Manager):
    
    def get_queryset(self):
        promo_ids = super(PromotionManagerByQuantity, self).get_queryset().filter(rules__by_qty=False,rules__by_amount=False,rules__by_products=True).values_list('pk', flat=True)
        return self.__class__.objects.filter(pk__in=promo_ids)
from django.db import models
from generics.models.base_entity import BaseEntity
from generics.models.sales.category import ProductCategory
from generics.models.sales.keyword import TagKeyword


class Product(BaseEntity):
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(ProductCategory)
    sale_available = models.BooleanField(default=True)
    rent_available = models.BooleanField(default=False)
    tags = models.ManyToManyField(TagKeyword)
    mfg_date = models.IntegerField(default=0)
    expire_date = models.IntegerField(default=0)

    @classmethod
    def apply_search(cls, queryset, request=None, **kwargs):
        if request and request.GET.get('id'):
            search_criteria = int(request.GET.get('id'))
            queryset = queryset.filter(pk=search_criteria)
        return queryset

    class Meta:
        abstract = True
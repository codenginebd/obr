from django.db import models
from django.template.defaultfilters import slugify

from generics.models.base_entity import BaseEntity
from generics.models.sales.category import ProductCategory
from generics.models.sales.keyword import TagKeyword
from generics.models.sales.product_images import ProductImage


class Product(BaseEntity):
    title = models.CharField(max_length=500)
    title_2 = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500)
    subtitle_2 = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    description_2 = models.TextField(blank=True)
    categories = models.ManyToManyField(ProductCategory)
    sale_available = models.BooleanField(default=True)
    rent_available = models.BooleanField(default=False)
    tags = models.ManyToManyField(TagKeyword)
    mfg_date = models.IntegerField(default=0)
    expire_date = models.IntegerField(default=0)
    slug = models.SlugField()
    images = models.ManyToManyField(ProductImage)

    @classmethod
    def apply_search(cls, queryset, request=None, **kwargs):
        if request and request.GET.get('id'):
            search_criteria = int(request.GET.get('id'))
            queryset = queryset.filter(pk=search_criteria)
        return queryset

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        super(Product, self).save(force_insert=force_insert, force_update=force_update, using=using,
             update_fields=update_fields)

    class Meta:
        abstract = True
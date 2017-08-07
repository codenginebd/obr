from django.db import models
from django.template.defaultfilters import slugify
from generics.models.base_entity import BaseEntity


class ProductCategory(BaseEntity):
    name = models.CharField(max_length=500)
    name_2 = models.CharField(max_length=500)
    show_name_2 = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductCategory, self).save(*args, **kwargs)

    @classmethod
    def get_all_parent_categories(cls, **kwargs):
        return cls.objects.filter(parent__isnull=True)

    @classmethod
    def get_all_descendants(cls, cat_id=None, **kwargs):
        pass
        
    @classmethod
    def get_all_children(cls, cat_id=None, **kwargs):
        all_categories = []
        
        if not cat_id:
            # For All Categories
            # Get All categories whose parent is None
            all_parent_categories = ProductCategory.objects.filter(parent__isnull=True)
            for parent_cat in all_parent_categories:
                direct_childs = ProductCategory.objects.filter(parent_id=parent_cat.pk)
                all_categories += [
                    {
                        "id": parent_cat.pk,
                        "name": parent_cat.name,
                        "slug": parent_cat.slug,
                        "instance": parent_cat,
                        "children": direct_childs
                    }
                ]
        else:
            parent_cat = ProductCategory.objects.get(pk=cat_id)
            direct_childs = ProductCategory.objects.filter(parent_id=cat_id)
            all_categories = {
                    "id": parent_cat.pk,
                    "name": parent_cat.name,
                    "slug": parent_cat.slug,
                    "instance": parent_cat,
                    "children": direct_childs
                }
            
        return all_categories
        
        


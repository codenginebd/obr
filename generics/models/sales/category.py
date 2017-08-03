from django.db import models
from django.template.defaultfilters import slugify
from generics.models.base_entity import BaseEntity


class ProductCategory(BaseEntity):
    name = models.CharField(max_length=500)
    parent = models.ForeignKey('self', null=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductCategory, self).save(*args, **kwargs)

    @classmethod
    def get_category_explorer_chain(cls, cat_id): # Get current cat to the top most parent and next child if any
        cat_chain = [ cat_id ]
        book_cat_object = ProductCategory.objects.get(pk=cat_id)
        while book_cat_object.parent:
            book_cat_object = ProductCategory.objects.get(pk=book_cat_object.parent_id)
            cat_chain += [ book_cat_object.pk ]

            # Include all siblings
            book_cat_childs = ProductCategory.objects.filter(parent_id=book_cat_object.pk).values_list('pk', flat=True)
            cat_chain += book_cat_childs

        book_cat_objects = ProductCategory.objects.filter(parent_id=cat_id)
        if book_cat_objects.exists():
            cat_chain += book_cat_objects.values_list('pk', flat=True)

        cat_chain = list(set(cat_chain))

        return cat_chain

    @classmethod
    def get_explored_chain(cls, cat_id):
        cat_chain = [cat_id]
        book_cat_object = ProductCategory.objects.get(pk=cat_id)
        while book_cat_object.parent:
            book_cat_object = ProductCategory.objects.get(pk=book_cat_object.parent_id)
            cat_chain += [book_cat_object.pk]
        cat_chain = list(set(cat_chain))

        return cat_chain

    @classmethod
    def category_explorer_slug_url_chain(cls, cat_ids=[]):
        cat_dict = {}

        all_cat_dict = {}
        book_cat_objects = ProductCategory.objects.all()
        cat_ids = book_cat_objects.values_list('pk', flat=True)
        if cat_ids:
            book_cat_objects = ProductCategory.objects.filter(pk__in=cat_ids)
            cat_ids = book_cat_objects.values_list('pk', flat=True)
        for cat_object in book_cat_objects:
            all_cat_dict[cat_object.pk] = cat_object

        for cat_id in cat_ids:
            cat_slug_chain = []
            book_cat_object = all_cat_dict[cat_id]
            cat_slug_chain += [book_cat_object.slug]
            while book_cat_object.parent:
                book_cat_object = all_cat_dict[book_cat_object.parent_id]
                cat_slug_chain += [book_cat_object.slug]

            # cat_slug_chain += [book_cat_object.slug]

            cat_slug_chain = cat_slug_chain[::-1]

            cat_dict[cat_id] = '/'.join(cat_slug_chain)

        return cat_dict

    @classmethod
    def get_all_subcategories(cls, main_categories, parent_categories={}):
        all_categories = []
        for cat_object in main_categories:
            childrens = parent_categories.get(cat_object.pk)
            # print(cat_object.pk)
            # print(childrens)
            cat_object = {
                "id": cat_object.pk,
                "name": cat_object.name,
                "parent": cat_object.parent,
                "children": []
            }
            if childrens:
                temp_categories = cls.get_all_subcategories(childrens, parent_categories)
                cat_object["children"] += temp_categories
            all_categories += [ cat_object ]
        return all_categories

    @classmethod
    def get_all_book_categories(cls, **kwargs):
        categories = {}

        all_categories = cls.objects.all() #.values_list('pk', 'name', 'parent_id')

        parents = {}

        for each_cat in all_categories:
            if each_cat.parent_id:
                if not each_cat.parent_id in parents.keys():
                    parents[each_cat.parent_id] = [ each_cat ]
                else:
                    parents[each_cat.parent_id] += [each_cat]

        cls.all_parents = parents

        main_categories = cls.objects.filter(parent__isnull=True) #.values_list('pk', 'name')

        print([ i.pk for i in main_categories ])

        cat_list = cls.get_all_subcategories(main_categories, parents)

        return cat_list
        
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
        
        


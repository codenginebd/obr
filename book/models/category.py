from django.db import models
from django.template.defaultfilters import slugify
from generics.models.base_entity import BaseEntity


class BookCategory(BaseEntity):
    name = models.CharField(max_length=500)
    parent = models.ForeignKey('self', null=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(BookCategory, self).save(*args, **kwargs)

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
                "children": childrens
            }
            if childrens:
                temp_categories = cls.get_all_subcategories(childrens, parent_categories)
                cat_object["children"] += temp_categories
            all_categories += [ cat_object ]
        return all_categories

    @classmethod
    def get_all_book_categories(cls, filter=None):
        categories = {}

        all_categories = cls.objects.all() #.values_list('pk', 'name', 'parent_id')

        parents = {}

        for each_cat in all_categories:
            if each_cat.parent_id:
                if not each_cat.parent_id in parents.keys():
                    parents[each_cat.parent_id] = [ each_cat ]
                else:
                    parents[each_cat.parent_id] += [each_cat]

        # print(parents)

        main_categories = cls.objects.filter(parent__isnull=True) #.values_list('pk', 'name')

        # print([ i.pk for i in main_categories ])

        cat_list = cls.get_all_subcategories(main_categories, parents)

        return cat_list


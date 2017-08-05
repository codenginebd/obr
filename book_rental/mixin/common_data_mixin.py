from book_rental.models.author import Author
from generics.models.sales.category import ProductCategory


class CommonDataMixin(object):

    def get_all_categories(self):
        return ProductCategory.get_all_children()

    def get_all_parent_categories(self):
        return ProductCategory.get_all_parent_categories()

    def get_all_children(self, cat_id=None, **kwargs):
        return ProductCategory.get_all_children(cat_id=cat_id, **kwargs)

    def get_all_authors(self):
        return Author.objects.all()
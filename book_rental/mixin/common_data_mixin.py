from book_rental.models.author import Author
from book_rental.models.book_publisher import BookPublisher
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

    def get_all_publishers(self):
        return BookPublisher.objects.all()
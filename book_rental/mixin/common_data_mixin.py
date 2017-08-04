from generics.models.sales.category import ProductCategory


class CommonDataMixin(object):

    def get_all_categories(self):
        return ProductCategory.get_all_children()
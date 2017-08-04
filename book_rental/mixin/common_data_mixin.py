from generics.models.sales.category import ProductCategory


class CommonDataMixin(object):

    def get_all_categories(self):
        return ProductCategory.get_all_children()

    def get_all_parent_categiries(self):
        return ProductCategory.get_all_parent_categories()
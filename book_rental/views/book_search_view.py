from ecommerce.models.sales.category import ProductCategory
from generics.views.base_template_view import BaseTemplateView


class BookSearchView(BaseTemplateView):
    template_name = "book_search.html"

    def get_filter_categories(self):
        cat_id = self.request.GET.get('cat')
        try:
            cat_id = int(cat_id)
        except Exception as exp:
            cat_id = None
        if not cat_id:
            return None, ProductCategory.get_all_parent_categories()
        else:
            parent_cat = ProductCategory.objects.get(pk=cat_id)
            return parent_cat, ProductCategory.get_all_children(cat_id=cat_id)

    def get_context_data(self, **kwargs):
        context = super(BookSearchView, self).get_context_data(**kwargs)
        context['page_title'] = 'Search Books'
        parent_cat, childrens = self.get_filter_categories()
        context['filter_categories'] = childrens
        context['parent_cat'] = parent_cat
        return context
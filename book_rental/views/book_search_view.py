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
            return ProductCategory.get_all_parent_categories()
        else:
            return ProductCategory.get_all_children(cat_id=cat_id)

    def get_context_data(self, **kwargs):
        context = super(BookSearchView, self).get_context_data(**kwargs)
        context['filter_categories'] = self.get_filter_categories()
        return context
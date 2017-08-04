from book_rental.mixin.common_data_mixin import CommonDataMixin
from generics.models.sales.category import ProductCategory
from generics.views.base_template_view import BaseTemplateView


class BookBrowseView(BaseTemplateView, CommonDataMixin):
    template_name = "book_browse.html"

    def get_context_data(self, **kwargs):
        context = super(BookBrowseView, self).get_context_data(**kwargs)
        context['page_title'] = 'Browse Books'

        slug = kwargs.get('slug')

        if slug:
            slug = slug.split('/')[-1:]
            if slug:
                slug = slug[0]

        book_category_objects = ProductCategory.objects.filter(slug=slug)

        context['all_categories'] = self.get_all_categories()

        return context

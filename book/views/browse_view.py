from book.models.category import BookCategory
from generics.views.base_template_view import BaseTemplateView


class BookBrowseView(BaseTemplateView):
    template_name = "book_browse.html"

    def get_context_data(self, **kwargs):
        context = super(BookBrowseView, self).get_context_data(**kwargs)
        context['page_title'] = 'Browse Books'

        slug = kwargs.get('slug')

        if slug:
            slug = slug.split('/')[-1:]
            if slug:
                slug = slug[0]

        book_category_objects = BookCategory.objects.filter(slug=slug)

        categories = BookCategory.get_all_book_categories()

        current_item_id = None

        if book_category_objects.exists():
            current_item_id = book_category_objects.first().pk
        else:
            if categories:
                current_item_id = categories[0]['id']

        context["categories"] = categories

        category_chain = BookCategory.get_category_explorer_chain(current_item_id)

        context["current_chain"] = category_chain

        context["current_item"] = current_item_id

        context["category_slug_urls"] = BookCategory.category_explorer_slug_url_chain()

        context["all_parents"] = BookCategory.all_parents

        context["explored_chain"] = BookCategory.get_explored_chain(current_item_id)

        return context

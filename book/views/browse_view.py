from django.views.generic.base import TemplateView

from book.models.category import BookCategory


class BookBrowseView(TemplateView):
    template_name = "book_browse.html"

    def get_context_data(self, **kwargs):
        context = super(BookBrowseView, self).get_context_data(**kwargs)
        context['page_title'] = 'Browse Books'

        context["categories"] = BookCategory.get_all_book_categories()

        return context
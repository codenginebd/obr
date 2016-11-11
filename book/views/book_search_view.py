from django.views.generic.base import TemplateView


class BookSearchView(TemplateView):
    template_name = "book_search.html"
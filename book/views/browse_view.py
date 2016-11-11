from django.views.generic.base import TemplateView


class BookBrowseView(TemplateView):
    template_name = "book_browse.html"
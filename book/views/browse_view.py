from django.views.generic.base import TemplateView


class BookBrowseView(TemplateView):
    template_name = "book_browse.html"

    def get_context_data(self, **kwargs):
        context = super(BookBrowseView, self).get_context_data(**kwargs)
        context['page_title'] = 'Browse Books'
        return context
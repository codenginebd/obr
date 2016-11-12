from django.views.generic.base import TemplateView


class BookDetailsView(TemplateView):
    template_name = "book_details.html"
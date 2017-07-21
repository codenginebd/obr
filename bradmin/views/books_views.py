from django.views.generic.base import TemplateView


class AdminBooksView(TemplateView):
    template_name = "admin/books_master.html"


class AdminBooksUploadView(TemplateView):
    template_name = "admin/books_upload.html"
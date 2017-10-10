from django.urls.base import reverse

from book_rental.models.sales.book import Book
from bradmin.views.activate_base_view import ActivateBaseView
from bradmin.views.base_list_view import BaseListView
from bradmin.views.deactivate_base_view import DeactivateBaseView
from bradmin.views.delete_base_view import DeleteBaseView
from bradmin.views.download_base_view import DownloadBaseView
from bradmin.views.upload_base_view import UploadBaseView


class AdminBooksListView(BaseListView):
    model = Book
    template_name = "admin/book/book_list.html"

    def show_upload(self):
        return True

    def show_download(self):
        return True

    def show_download_template(self):
        return True

    def get_breadcumb(self, request):
        return [

        ]

    def get_ttab_name(self):
        return "book"

    def get_ltab_name(self):
        return "All"

    def apply_filter(self, request, queryset):
        return queryset

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_book_list_view"),
            "Error Logs": reverse("admin_error_logs_view")+"?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Book List | BDReads.com"


class AdminBookUploadView(UploadBaseView):
    model = Book


class AdminBookDownloadView(DownloadBaseView):
    model = Book


class AdminBookActivateView(ActivateBaseView):
    model = Book


class AdminBookDeactivateView(DeactivateBaseView):
    model = Book


class AdminBookDeleteView(DeleteBaseView):
    model = Book
from django.urls.base import reverse

from book_rental.models.author import Author
from book_rental.models.book_publisher import BookPublisher
from book_rental.models.sales.book import Book
from bradmin.views.base_detail_view import BaseDetailView
from bradmin.views.base_list_view import BaseListView
from ecommerce.models.sales.category import ProductCategory
from ecommerce.models.sales.warehouse import Warehouse
from logger.models.error_log import ErrorLog


class AdminErrorLogView(BaseListView):
    model = ErrorLog
    template_name = "admin/errorlog_list.html"

    def get_left_menu_items(self):
        context = self.request.GET.get('context', None)
        error_log_url = reverse("admin_error_logs_view")
        if context:
            error_log_url +=  "?context=%s" % self.request.GET.get('context')
        all_url = ""
        if context == ProductCategory.__name__:
            all_url = reverse("admin_category_view")
        elif context == BookPublisher.__name__:
            all_url = reverse("admin_publishers_view")
        elif context == Book.__name__:
            all_url = reverse("admin_book_list_view")
        elif context == Author.__name__:
            all_url = reverse("admin_author_list_view")
        elif context == Warehouse.__name__:
            all_url = reverse("admin_warehouse_list_view")
        return {
            "All": all_url,
            "Error Logs": error_log_url
        }

    def get_page_title(self):
        return "Category Logs"

    def get_table_headers(self):
        return [
            "ID", "Code", "context", "url", "stacktrace", "Details"
        ]

    def prepare_table_data(self, queryset):
        data = []
        for q_object in queryset:
            data += [
                [
                    q_object.pk, q_object.code, q_object.context if q_object.context else "-",
                    q_object.url if q_object.url else "-",
                    q_object.stacktrace if q_object.stacktrace else "-",
                    '<a href="%s">Details</a>' % q_object.get_detail_link(object_id=q_object.pk)
                ]
            ]
        return data

    def get_ttab_name(self):
        context = self.request.GET.get('context', '')
        if context == ProductCategory.__name__:
            return "category"
        elif context == BookPublisher.__name__:
            return "publisher"
        elif context == Book.__name__:
            return "book"
        elif context == Author.__name__:
            return "author"
        elif context == Warehouse.__name__:
            return "warehouse"

    def get_ltab_name(self):
        return "Error Logs"


class AdminErrorLogsDetailsView(BaseDetailView):
    model = ErrorLog

    def get_template_names(self):
        return [
            "admin/admin_error_log_details.html"
        ]

    def get_page_title(self):
        return "Error Log Details | BDReads.com"
from django.urls.base import reverse

from bradmin.views.base_detail_view import BaseDetailView
from bradmin.views.base_list_view import BaseListView
from ecommerce.models.sales.category import ProductCategory
from logger.models.error_log import ErrorLog


class AdminErrorLogView(BaseListView):
    model = ErrorLog
    template_name = "admin/errorlog_list.html"

    def get_left_menu_items(self):
        error_log_url = reverse("admin_error_logs_view")
        if self.request.GET.get('context', None):
            error_log_url +=  "?context=%s" % self.request.GET.get('context')
        return {
            "All": reverse("admin_category_view"),
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
        if self.request.GET.get('context', '') == ProductCategory.__name__:
            return "category"

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
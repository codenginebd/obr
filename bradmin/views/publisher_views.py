from django.urls.base import reverse

from book_rental.models.book_publisher import BookPublisher
from bradmin.views.base_list_view import BaseListView


class AdminPublisherListView(BaseListView):
    model = BookPublisher
    template_name = "admin/publisher/publisher_list.html"

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
        return "publisher"

    def get_ltab_name(self):
        return "All"

    def apply_filter(self, request, queryset):
        return queryset

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_publishers_view"),
            "Error Logs": reverse("admin_error_logs_view")+"?context=%s" % self.model.__name__
        }

    def get_table_headers(self):
        return [
            "ID", "Code", "Name(English)", "Name(Bangla)", "Active?", "Show Bangla", "Parent", "Details"
        ]

    def prepare_table_data(self, queryset):
        data = []
        for q_object in queryset:
            data += [
                [
                    q_object.pk, q_object.code, q_object.name, q_object.name_2, q_object.is_active,
                    True if q_object.show_name_2 else False,
                    q_object.parent.name if q_object.parent else "-",
                    '<a href="%s">Details</a>' % q_object.get_detail_link(object_id=q_object.pk)
                ]
            ]
        return data

    def get_page_title(self):
        return "Publisher List | BDReads.com"
from django.urls.base import reverse

from book_rental.models.book_publisher import BookPublisher
from bradmin.forms.publisher_form import AdminBookPublisherForm
from bradmin.views.activate_base_view import ActivateBaseView
from bradmin.views.base_create_view import BRBaseCreateView
from bradmin.views.base_detail_view import BaseDetailView
from bradmin.views.base_list_view import BaseListView
from bradmin.views.base_update_view import BRBaseUpdateView
from bradmin.views.deactivate_base_view import DeactivateBaseView
from bradmin.views.delete_base_view import DeleteBaseView
from bradmin.views.download_base_view import DownloadBaseView
from bradmin.views.upload_base_view import UploadBaseView


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
            "ID", "Code", "Name(English)", "Name(Bangla)", "Active?", "Show Bangla", "Details"
        ]

    def prepare_table_data(self, queryset):
        data = []
        for q_object in queryset:
            data += [
                [
                    q_object.pk, q_object.code, q_object.name, q_object.name_2, q_object.is_active,
                    True if q_object.show_2 else False,
                    '<a href="%s">Details</a>' % q_object.get_detail_link(object_id=q_object.pk)
                ]
            ]
        return data

    def get_page_title(self):
        return "Publisher List | BDReads.com"


class AdminBookPublisherUploadView(UploadBaseView):
    model = BookPublisher


class AdminBookPublisherDownloadView(DownloadBaseView):
    model = BookPublisher


class AdminBookPublisherActivateView(ActivateBaseView):
    model = BookPublisher


class AdminBookPublisherDeactivateView(DeactivateBaseView):
    model = BookPublisher


class AdminBookPublisherDeleteView(DeleteBaseView):
    model = BookPublisher


class AdminBookPublisherDetailsView(BaseDetailView):
    model = BookPublisher

    def get_template_names(self):
        return [
            "admin/publisher/admin_publisher_details.html"
        ]

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_publishers_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Publisher Details | BDReads.com"

    def get_ttab_name(self):
        return "publisher"


class AdminBookPublisherCreateView(BRBaseCreateView):
    form_class =BookPublisher
    template_name = "admin/admin_category_create.html"

    def get_form_title(self):
        return "Category Create"

    def get_success_url(self):
        return reverse("admin_category_view")

    def get_cancel_url(self):
        return reverse("admin_category_view")

    def get_page_title(self):
        return "Create Category | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_category_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % ProductCategory.__name__
        }


class AdminBookPublisherUpdateView(BRBaseUpdateView):
    form_class = AdminBookPublisherForm
    queryset = BookPublisher.objects.all()
    template_name = "admin/admin_category_create.html"

    def get_form_title(self):
        return "Category Update(#%s)" % self.object.pk

    def get_success_url(self):
        return reverse("admin_category_view")

    def get_cancel_url(self):
        return reverse("admin_category_view")

    def get_page_title(self):
        return "Update Category | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_category_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % ProductCategory.__name__
        }
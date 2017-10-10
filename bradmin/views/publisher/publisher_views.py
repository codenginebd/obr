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
    form_class =AdminBookPublisherForm
    template_name = "admin/publisher/admin_publisher_create.html"

    def get_form_title(self):
        return "Publisher Create"

    def get_success_url(self):
        return reverse("admin_publishers_view")

    def get_cancel_url(self):
        return reverse("admin_publishers_view")

    def get_page_title(self):
        return "Create Publisher | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_publishers_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % BookPublisher.__name__
        }


class AdminBookPublisherUpdateView(BRBaseUpdateView):
    form_class = AdminBookPublisherForm
    queryset = BookPublisher.objects.all()
    template_name = "admin/publisher/admin_publisher_create.html"

    def get_form_title(self):
        return "Publisher Update(#%s)" % self.object.pk

    def get_success_url(self):
        return reverse("admin_publishers_view")

    def get_cancel_url(self):
        return reverse("admin_publishers_view")

    def get_page_title(self):
        return "Update Publisher | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_publishers_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % BookPublisher.__name__
        }
from django.urls.base import reverse

from book_rental.models.author import Author
from bradmin.forms.author_forms import AdminAuthorForm
from bradmin.views.activate_base_view import ActivateBaseView
from bradmin.views.base_create_view import BRBaseCreateView
from bradmin.views.base_detail_view import BaseDetailView
from bradmin.views.base_list_view import BaseListView
from bradmin.views.base_update_view import BRBaseUpdateView
from bradmin.views.deactivate_base_view import DeactivateBaseView
from bradmin.views.delete_base_view import DeleteBaseView
from bradmin.views.download_base_view import DownloadBaseView
from bradmin.views.upload_base_view import UploadBaseView


class AdminAuthorListView(BaseListView):
    model = Author
    template_name = "admin/author/author_list.html"

    def get_breadcumb(self, request):
        return [

        ]

    def get_ttab_name(self):
        return "author"

    def get_ltab_name(self):
        return "All"

    def apply_filter(self, request, queryset):
        return queryset

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_author_list_view"),
            "Error Logs": reverse("admin_error_logs_view")+"?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Author List | BDReads.com"


class AdminAuthorUploadView(UploadBaseView):
    model = Author


class AdminAuthorDownloadView(DownloadBaseView):
    model = Author


class AdminAuthorActivateView(ActivateBaseView):
    model = Author


class AdminAuthorDeactivateView(DeactivateBaseView):
    model = Author


class AdminAuthorDeleteView(DeleteBaseView):
    model = Author


class AdminBAuthorDetailsView(BaseDetailView):
    model = Author

    def get_template_names(self):
        return [
            "admin/author/admin_author_details.html"
        ]

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_author_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Author Details | BDReads.com"

    def get_ttab_name(self):
        return "author"


class AdminAuthorCreateView(BRBaseCreateView):
    form_class =AdminAuthorForm
    template_name = "admin/author/admin_author_create.html"

    def get_form_title(self):
        return "Author Create"

    def get_success_url(self):
        return reverse("admin_author_list_view")

    def get_cancel_url(self):
        return reverse("admin_author_list_view")

    def get_page_title(self):
        return "Create Author | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_author_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % Author.__name__
        }


class AdminAuthorUpdateView(BRBaseUpdateView):
    form_class = AdminAuthorForm
    queryset = Author.objects.all()
    template_name = "admin/author/admin_author_create.html"

    def get_form_title(self):
        return "Author Update(#%s)" % self.object.pk

    def get_success_url(self):
        return reverse("admin_author_list_view")

    def get_cancel_url(self):
        return reverse("admin_author_list_view")

    def get_page_title(self):
        return "Update Author | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_author_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % Author.__name__
        }
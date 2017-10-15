from django.urls.base import reverse

from bradmin.forms.admin_front_list_forms import AdminFrontListForm
from bradmin.views.activate_base_view import ActivateBaseView
from bradmin.views.base_create_view import BRBaseCreateView
from bradmin.views.base_detail_view import BaseDetailView
from bradmin.views.base_list_view import BaseListView
from bradmin.views.base_update_view import BRBaseUpdateView
from bradmin.views.deactivate_base_view import DeactivateBaseView
from bradmin.views.delete_base_view import DeleteBaseView
from ecommerce.models.front_list import FrontList


class AdminFrontListListView(BaseListView):
    model = FrontList
    template_name = "admin/frontlist/frontlist_list.html"

    def get_breadcumb(self, request):
        return [

        ]

    def get_ttab_name(self):
        return "frontlist"

    def get_ltab_name(self):
        return "All"

    def apply_filter(self, request, queryset):
        return queryset

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_frontlist_list_view"),
            "Error Logs": reverse("admin_error_logs_view")+"?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Front List | BDReads.com"


class AdminFrontListDetailsView(BaseDetailView):
    model = FrontList

    def get_template_names(self):
        return [
            "admin/frontlist/admin_front_list_details.html"
        ]

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_frontlist_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Front List Details | BDReads.com"

    def get_ttab_name(self):
        return "frontlist"


class AdminFrontListActivateView(ActivateBaseView):
    model = FrontList


class AdminFrontListDeactivateView(DeactivateBaseView):
    model = FrontList


class AdminFrontListDeleteView(DeleteBaseView):
    model = FrontList


class AdminFrontListCreateView(BRBaseCreateView):
    form_class =AdminFrontListForm
    template_name = "admin/frontlist/admin_front_list_create.html"

    def get_form_title(self):
        return "Front List Create"

    def get_success_url(self):
        return reverse("admin_frontlist_list_view")

    def get_cancel_url(self):
        return reverse("admin_frontlist_list_view")

    def get_page_title(self):
        return "Create Front List | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_frontlist_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % FrontList.__name__
        }


class AdminFrontListUpdateView(BRBaseUpdateView):
    form_class = AdminFrontListForm
    template_name = "admin/frontlist/admin_front_list_create.html"
    queryset = FrontList.objects.all()

    def get_form_title(self):
        return "Frot List Update(#%s)" % self.object.pk

    def get_success_url(self):
        return reverse("admin_frontlist_list_view")

    def get_cancel_url(self):
        return reverse("admin_frontlist_list_view")

    def get_page_title(self):
        return "Update Front List | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_frontlist_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % FrontList.__name__
        }
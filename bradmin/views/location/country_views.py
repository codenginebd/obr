from django.urls.base import reverse

from bauth.models.country import Country
from bradmin.forms.location_forms import AdminCountryForm
from bradmin.views.activate_base_view import ActivateBaseView
from bradmin.views.base_create_view import BRBaseCreateView
from bradmin.views.base_list_view import BaseListView
from bradmin.views.base_update_view import BRBaseUpdateView
from bradmin.views.deactivate_base_view import DeactivateBaseView
from bradmin.views.delete_base_view import DeleteBaseView


class AdminCountryListView(BaseListView):
    model = Country
    template_name = "admin/location/admin_location_list.html"

    def get_breadcumb(self, request):
        return [

        ]

    def get_ttab_name(self):
        return "country"

    def get_ltab_name(self):
        return "All"

    def apply_filter(self, request, queryset):
        return queryset

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_country_list_view"),
            "Error Logs": reverse("admin_error_logs_view")+"?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Country List | BDReads.com"


class AdminCountryActivateView(ActivateBaseView):
    model = Country


class AdminCountryDeactivateView(DeactivateBaseView):
    model = Country


class AdminCountryDeleteView(DeleteBaseView):
    model = Country


class AdminCountryCreateView(BRBaseCreateView):
    form_class =AdminCountryForm
    template_name = "admin/location/admin_location_create.html"

    def get_form_title(self):
        return "Country Create"

    def get_success_url(self):
        return reverse("admin_country_list_view")

    def get_cancel_url(self):
        return reverse("admin_country_list_view")

    def get_page_title(self):
        return "Create Country | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_country_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % Country.__name__
        }


class AdminCountryUpdateView(BRBaseUpdateView):
    form_class = AdminCountryForm
    queryset = Country.objects.all()
    template_name = "admin/location/admin_location_create.html"

    def get_form_title(self):
        return "Country Update(#%s)" % self.object.pk

    def get_success_url(self):
        return reverse("admin_country_list_view")

    def get_cancel_url(self):
        return reverse("admin_country_list_view")

    def get_page_title(self):
        return "Update Country | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_country_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % Country.__name__
        }
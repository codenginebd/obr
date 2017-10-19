from django.urls.base import reverse

from bradmin.forms.admin_rent_plan_relation_forms import AdminRentPlanForm
from bradmin.views.activate_base_view import ActivateBaseView
from bradmin.views.base_create_view import BRBaseCreateView
from bradmin.views.base_list_view import BaseListView
from bradmin.views.base_update_view import BRBaseUpdateView
from bradmin.views.deactivate_base_view import DeactivateBaseView
from bradmin.views.delete_base_view import DeleteBaseView
from ecommerce.models.rent_plan import RentPlan


class AdminRentPlanListView(BaseListView):
    model = RentPlan
    template_name = "admin/productprice/rent_plan_list.html"

    def get_breadcumb(self, request):
        return [

        ]

    def get_ttab_name(self):
        return "rentplan"

    def get_ltab_name(self):
        return "All"

    def apply_filter(self, request, queryset):
        return queryset

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_rent_plan_list_view"),
            "Error Logs": reverse("admin_error_logs_view")+"?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Rent Plan List | BDReads.com"


class AdminRentPlanActivateView(ActivateBaseView):
    model = RentPlan


class AdminRentPlanDeactivateView(DeactivateBaseView):
    model = RentPlan


class AdminRentPlanDeleteView(DeleteBaseView):
    model = RentPlan


class AdminRentPlanCreateView(BRBaseCreateView):
    form_class =AdminRentPlanForm
    template_name = "admin/productprice/admin_rent_plan_create.html"

    def get_form_title(self):
        return "Rent Plan Create"

    def get_success_url(self):
        return reverse("admin_rent_plan_list_view")

    def get_cancel_url(self):
        return reverse("admin_rent_plan_list_view")

    def get_page_title(self):
        return "Create Rent Plan | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_rent_plan_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % RentPlan.__name__
        }


class AdminRentPlanUpdateView(BRBaseUpdateView):
    form_class = AdminRentPlanForm
    queryset = RentPlan.objects.all()
    template_name = "admin/productprice/admin_rent_plan_create.html"

    def get_form_title(self):
        return "Rent Plan Update(#%s)" % self.object.pk

    def get_success_url(self):
        return reverse("admin_rent_plan_list_view")

    def get_cancel_url(self):
        return reverse("admin_rent_plan_list_view")

    def get_page_title(self):
        return "Update Rent Plan | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_rent_plan_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % RentPlan.__name__
        }
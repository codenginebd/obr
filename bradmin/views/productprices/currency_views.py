from django.urls.base import reverse

from bradmin.forms.admin_currency_forms import AdminCurrencyForm
from bradmin.views.activate_base_view import ActivateBaseView
from bradmin.views.base_create_view import BRBaseCreateView
from bradmin.views.base_list_view import BaseListView
from bradmin.views.base_update_view import BRBaseUpdateView
from bradmin.views.deactivate_base_view import DeactivateBaseView
from bradmin.views.delete_base_view import DeleteBaseView
from payment.models.currency import Currency


class AdminCurrencyListView(BaseListView):
    model = Currency
    template_name = "admin/productprice/admin_currency_list.html"

    def get_breadcumb(self, request):
        return [

        ]

    def get_ttab_name(self):
        return "currency"

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
        return "Currency List | BDReads.com"


class AdminCurrencyActivateView(ActivateBaseView):
    model = Currency


class AdminCurrencyDeactivateView(DeactivateBaseView):
    model = Currency


class AdminCurrencyDeleteView(DeleteBaseView):
    model = Currency


class AdminCurrencyCreateView(BRBaseCreateView):
    form_class =AdminCurrencyForm
    template_name = "admin/productprice/admin_currency_create.html"

    def get_form_title(self):
        return "Currency Create"

    def get_success_url(self):
        return reverse("admin_currency_list_view")

    def get_cancel_url(self):
        return reverse("admin_currency_list_view")

    def get_page_title(self):
        return "Create Currency | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_currency_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % Currency.__name__
        }


class AdminCurrencyUpdateView(BRBaseUpdateView):
    form_class = AdminCurrencyForm
    queryset = Currency.objects.all()
    template_name = "admin/productprice/admin_currency_create.html"

    def get_form_title(self):
        return "Currency Update(#%s)" % self.object.pk

    def get_success_url(self):
        return reverse("admin_currency_list_view")

    def get_cancel_url(self):
        return reverse("admin_currency_list_view")

    def get_page_title(self):
        return "Update Currency | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_currency_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % Currency.__name__
        }
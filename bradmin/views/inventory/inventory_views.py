from django.urls.base import reverse
from bradmin.forms.admin_inventory_forms import AdminInventoryForm
from bradmin.views.activate_base_view import ActivateBaseView
from bradmin.views.base_create_view import BRBaseCreateView
from bradmin.views.base_detail_view import BaseDetailView
from bradmin.views.base_list_view import BaseListView
from bradmin.views.base_update_view import BRBaseUpdateView
from bradmin.views.deactivate_base_view import DeactivateBaseView
from bradmin.views.delete_base_view import DeleteBaseView
from bradmin.views.download_base_view import DownloadBaseView
from bradmin.views.upload_base_view import UploadBaseView
from inventory.models.inventory import Inventory


class AdminInventoryListView(BaseListView):
    model = Inventory
    template_name = "admin/inventory/inventory_list.html"

    def get_breadcumb(self, request):
        return [

        ]

    def get_ttab_name(self):
        return "inventory"

    def get_ltab_name(self):
        return "All"

    def apply_filter(self, request, queryset):
        return queryset

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_inventory_list_view"),
            'Inventory Alert': reverse("admin_inventory_alert_list_view"),
            "Error Logs": reverse("admin_error_logs_view")+"?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Inventory List | BDReads.com"


class AdminInventoryAlertListView(BaseListView):
    model = Inventory
    template_name = "admin/inventory/inventory_list.html"

    def get_breadcumb(self, request):
        return [

        ]

    def get_ttab_name(self):
        return "inventory"

    def get_ltab_name(self):
        return "Inventory Alert"

    def apply_filter(self, request, queryset):
        queryset = queryset.filter(stock__lte=5)
        return queryset

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_inventory_list_view"),
            'Inventory Alert': reverse("admin_inventory_alert_list_view"),
            "Error Logs": reverse("admin_error_logs_view")+"?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Inventory Alerts | BDReads.com"


class AdminInventoryUploadView(UploadBaseView):
    model = Inventory


class AdminInventoryDownloadView(DownloadBaseView):
    model = Inventory


class AdminInventoryActivateView(ActivateBaseView):
    model = Inventory


class AdminInventoryDeactivateView(DeactivateBaseView):
    model = Inventory


class AdminInventoryDeleteView(DeleteBaseView):
    model = Inventory


class AdminInventoryDetailsView(BaseDetailView):
    model = Inventory

    def get_template_names(self):
        return [
            "admin/inventory/admin_inventory_details.html"
        ]

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_inventory_list_view"),
            'Inventory Alert': reverse("admin_inventory_alert_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Inventory Details | BDReads.com"

    def get_ttab_name(self):
        return "inventory"


class AdminInventoryCreateView(BRBaseCreateView):
    form_class =AdminInventoryForm
    template_name = "admin/inventory/admin_inventory_create.html"

    def get_form_title(self):
        return "Inventory Create"

    def get_success_url(self):
        return reverse("admin_inventory_list_view")

    def get_cancel_url(self):
        return reverse("admin_inventory_list_view")

    def get_page_title(self):
        return "Create Inventory | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_inventory_list_view"),
            'Inventory Alert': reverse("admin_inventory_alert_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % Inventory.__name__
        }


class AdminInventoryUpdateView(BRBaseUpdateView):
    form_class = AdminInventoryForm
    queryset = Inventory.objects.all()
    template_name = "admin/inventory/admin_inventory_create.html"

    def get_form_title(self):
        return "Inventory Update(#%s)" % self.object.pk

    def get_success_url(self):
        return reverse("admin_inventory_list_view")

    def get_cancel_url(self):
        return reverse("admin_inventory_list_view")

    def get_page_title(self):
        return "Update Inventory | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_inventory_list_view"),
            'Inventory Alert': reverse("admin_inventory_alert_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % Inventory.__name__
        }
from django.urls.base import reverse
from bradmin.forms.admin_inventory_forms import AdminInventoryForm
from bradmin.views.base_create_view import BRBaseCreateView
from bradmin.views.base_list_view import BaseListView
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
            "Error Logs": reverse("admin_error_logs_view")+"?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Inventory List | BDReads.com"


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
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % Inventory.__name__
        }
from django.urls.base import reverse

from bradmin.forms.admin_warehouse_form import AdminWarehouseForm
from bradmin.views.activate_base_view import ActivateBaseView
from bradmin.views.base_create_view import BRBaseCreateView
from bradmin.views.base_detail_view import BaseDetailView
from bradmin.views.base_list_view import BaseListView
from bradmin.views.base_update_view import BRBaseUpdateView
from bradmin.views.deactivate_base_view import DeactivateBaseView
from bradmin.views.delete_base_view import DeleteBaseView
from bradmin.views.download_base_view import DownloadBaseView
from bradmin.views.upload_base_view import UploadBaseView
from ecommerce.models.sales.warehouse import Warehouse


class AdminWarehouseListView(BaseListView):
    model = Warehouse
    template_name = "admin/warehouse/warehouse_list.html"

    def get_breadcumb(self, request):
        return [

        ]

    def get_ttab_name(self):
        return "warehouse"

    def get_ltab_name(self):
        return "All"

    def apply_filter(self, request, queryset):
        return queryset

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_warehouse_list_view"),
            "Error Logs": reverse("admin_error_logs_view")+"?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Warehouse List | BDReads.com"


class AdminWarehouseUploadView(UploadBaseView):
    model = Warehouse


class AdminWarehouseDownloadView(DownloadBaseView):
    model = Warehouse


class AdminWarehouseActivateView(ActivateBaseView):
    model = Warehouse


class AdminWarehouseDeactivateView(DeactivateBaseView):
    model = Warehouse


class AdminWarehouseDeleteView(DeleteBaseView):
    model = Warehouse


class AdminDetailsDetailsView(BaseDetailView):
    model = Warehouse

    def get_template_names(self):
        return [
            "admin/warehouse/admin_warehouse_details.html"
        ]

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_warehouse_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Warehouse Details | BDReads.com"

    def get_ttab_name(self):
        return "warehouse"


class AdminWarehouseCreateView(BRBaseCreateView):
    form_class =AdminWarehouseForm
    template_name = "admin/warehouse/admin_warehouse_create.html"

    def get_form_title(self):
        return "Warehouse Create"

    def get_success_url(self):
        return reverse("admin_warehouse_list_view")

    def get_cancel_url(self):
        return reverse("admin_warehouse_list_view")

    def get_page_title(self):
        return "Create Warehouse | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_warehouse_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % Warehouse.__name__
        }


class AdminWarehouseUpdateView(BRBaseUpdateView):
    form_class = AdminWarehouseForm
    queryset = Warehouse.objects.all()
    template_name = "admin/warehouse/admin_warehouse_create.html"

    def get_form_title(self):
        return "Warehouse Update(#%s)" % self.object.pk

    def get_success_url(self):
        return reverse("admin_warehouse_list_view")

    def get_cancel_url(self):
        return reverse("admin_warehouse_list_view")

    def get_page_title(self):
        return "Update Warehouse | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_warehouse_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % Warehouse.__name__
        }
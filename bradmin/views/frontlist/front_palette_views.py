from django.urls.base import reverse

from bradmin.forms.admin_front_palette_forms import AdminFrontPaletteForm
from bradmin.views.activate_base_view import ActivateBaseView
from bradmin.views.base_create_view import BRBaseCreateView
from bradmin.views.base_detail_view import BaseDetailView
from bradmin.views.base_list_view import BaseListView
from bradmin.views.base_update_view import BRBaseUpdateView
from bradmin.views.deactivate_base_view import DeactivateBaseView
from bradmin.views.delete_base_view import DeleteBaseView
from bradmin.views.download_base_view import DownloadBaseView
from bradmin.views.upload_base_view import UploadBaseView
from ecommerce.models.front_palette import FrontPalette


class AdminFrontPaletteListView(BaseListView):
    model = FrontPalette
    template_name = "admin/frontlist/front_palette_list.html"

    def get_breadcumb(self, request):
        return [

        ]

    def get_ttab_name(self):
        return "frontpalette"

    def get_ltab_name(self):
        return "All"

    def apply_filter(self, request, queryset):
        return queryset

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_front_palette_list_view"),
            "Error Logs": reverse("admin_error_logs_view")+"?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Front Palette | BDReads.com"


class AdminFrontPaletteDetailsView(BaseDetailView):
    model = FrontPalette

    def get_template_names(self):
        return [
            "admin/frontlist/admin_front_palette_details.html"
        ]

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_front_palette_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Front Palette Details | BDReads.com"

    def get_ttab_name(self):
        return "frontpalette"


class AdminFrontPaletteActivateView(ActivateBaseView):
    model = FrontPalette


class AdminFrontPaletteDeactivateView(DeactivateBaseView):
    model = FrontPalette


class AdminFrontPaletteDeleteView(DeleteBaseView):
    model = FrontPalette


class AdminFrontPaletteCreateView(BRBaseCreateView):
    form_class =AdminFrontPaletteForm
    template_name = "admin/frontlist/admin_front_palette_create.html"

    def get_form_title(self):
        return "Front Palette Create"

    def get_success_url(self):
        return reverse("admin_front_palette_list_view")

    def get_cancel_url(self):
        return reverse("admin_front_palette_list_view")

    def get_page_title(self):
        return "Create Front Palette | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_front_palette_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % FrontPalette.__name__
        }


class AdminFrontPaletteUpdateView(BRBaseUpdateView):
    form_class = AdminFrontPaletteForm
    queryset = FrontPalette.objects.all()
    template_name = "admin/warehouse/admin_warehouse_create.html"

    def get_form_title(self):
        return "Front Palette Update(#%s)" % self.object.pk

    def get_success_url(self):
        return reverse("admin_front_palette_list_view")

    def get_cancel_url(self):
        return reverse("admin_front_palette_list_view")

    def get_page_title(self):
        return "Update Front Palette | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_front_palette_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % FrontPalette.__name__
        }
from django.urls.base import reverse
from django.views.generic.base import TemplateView

from bradmin.views.activate_base_view import ActivateBaseView
from bradmin.views.base_detail_view import BaseDetailView
from bradmin.views.base_list_view import BaseListView
from bradmin.views.deactivate_base_view import DeactivateBaseView
from bradmin.views.delete_base_view import DeleteBaseView
from bradmin.views.download_base_view import DownloadBaseView
from bradmin.views.upload_base_view import UploadBaseView
from ecommerce.models.sales.category import ProductCategory


class AdminCategoryView(TemplateView):
    template_name = "admin/category_master.html"


class AdminCategoryListView(BaseListView):
    model = ProductCategory
    template_name = "admin/category_list.html"

    def show_upload(self):
        return True

    def show_download(self):
        return True

    def show_download_template(self):
        return True

    def show_edit(self):
        return True

    def show_delete(self):
        return True

    def show_activate(self):
        return True

    def show_deactivate(self):
        return True

    def get_breadcumb(self, request):
        return [

        ]

    def apply_filter(self, request, queryset):
        return queryset

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_category_view"),
            "Error Logs": reverse("admin_category_logs_view")+"?context=%s" % self.model.__name__
        }

    def get_table_headers(self):
        return [
            "ID", "Code", "Name(English)", "Name(Bangla)", "Active?", "Show Bangla", "Parent", "Details"
        ]

    def prepare_table_data(self, queryset):
        data = []
        for q_object in queryset:
            data += [
                [
                    q_object.pk, q_object.code, q_object.name, q_object.name_2, q_object.is_active,
                    True if q_object.show_name_2 else False,
                    q_object.parent.name if q_object.parent else "-",
                    '<a href="%s">Details</a>' % q_object.get_detail_link(object_id=q_object.pk)
                ]
            ]
        return data


class AdminCategoryUploadView(UploadBaseView):
    model = ProductCategory


class AdminCategoryDownloadView(DownloadBaseView):
    model = ProductCategory


class AdminCategoryActivateView(ActivateBaseView):
    model = ProductCategory


class AdminCategoryDeactivateView(DeactivateBaseView):
    model = ProductCategory


class AdminCategoryDeleteView(DeleteBaseView):
    model = ProductCategory


class AdminCategoryDetailsView(BaseDetailView):
    model = ProductCategory

    def get_template_names(self):
        return [
            "admin/admin_category_details.html"
        ]
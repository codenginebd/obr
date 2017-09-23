from django.urls.base import reverse
from django.views.generic.base import TemplateView
from bradmin.views.base_list_view import BaseListView
from bradmin.views.download_base_view import DownloadBaseView
from bradmin.views.upload_base_view import UploadBaseView
from ecommerce.models.sales.category import ProductCategory


class AdminCategoryView(TemplateView):
    template_name = "admin/category_master.html"


class AdminCategoryListView(BaseListView):
    model = ProductCategory
    template_name = "admin/category_list.html"

    def get_breadcumb(self, request):
        return [

        ]

    def apply_filter(self, request, queryset):
        return queryset

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_category_view"),
            "Error Logs": reverse("admin_logs_view")+"?context=%s" % self.model.__name__
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
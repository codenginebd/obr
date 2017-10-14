from django.urls.base import reverse
from bradmin.views.base_list_view import BaseListView
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
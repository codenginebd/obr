from django.urls.base import reverse

from bradmin.forms.admin_product_price_forms import AdminProductPriceForm
from bradmin.forms.admin_rent_plan_relation_forms import AdminRentPlanRelationForm
from bradmin.views.base_create_view import BRBaseCreateView
from bradmin.views.base_list_view import BaseListView
from ecommerce.models.sales.price_matrix import PriceMatrix


class AdminRentPlanListView(BaseListView):
    model = PriceMatrix
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
            "All": reverse("admin_product_price_list_view"),
            "Error Logs": reverse("admin_error_logs_view")+"?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Rent Plan List | BDReads.com"
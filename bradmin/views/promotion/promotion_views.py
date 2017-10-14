from django.urls.base import reverse

from bradmin.forms.admin_promotion_forms import AdminPromotionForm
from bradmin.views.base_create_view import BRBaseCreateView
from bradmin.views.base_list_view import BaseListView
from promotion.models.promotion import Promotion


class AdminPromotionListView(BaseListView):
    model = Promotion
    template_name = "admin/promotion/promotion_list.html"

    def get_breadcumb(self, request):
        return [

        ]

    def get_ttab_name(self):
        return "promotion"

    def get_ltab_name(self):
        return "All"

    def apply_filter(self, request, queryset):
        return queryset

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_promotion_list_view"),
            "Error Logs": reverse("admin_error_logs_view")+"?context=%s" % self.model.__name__
        }

    def get_page_title(self):
        return "Promotion List | BDReads.com"


class AdminPromotionCreateView(BRBaseCreateView):
    form_class =AdminPromotionForm
    template_name = "admin/promotion/admin_promotion_create.html"

    def get_form_title(self):
        return "Promotion Create"

    def get_success_url(self):
        return reverse("admin_promotion_list_view")

    def get_cancel_url(self):
        return reverse("admin_promotion_list_view")

    def get_page_title(self):
        return "Create Promotion | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_promotion_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % Promotion.__name__
        }
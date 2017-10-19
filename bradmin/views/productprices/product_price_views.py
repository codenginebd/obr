from django.forms.formsets import formset_factory
from django.urls.base import reverse

from bradmin.forms.admin_product_price_forms import AdminProductPriceForm
from bradmin.forms.admin_rent_plan_relation_forms import AdminRentPlanRelationForm, AdminRentPlanFormSet
from bradmin.views.base_create_view import BRBaseCreateView
from bradmin.views.base_list_view import BaseListView
from ecommerce.models.rent_plan import RentPlan
from ecommerce.models.sales.price_matrix import PriceMatrix


class AdminProductPriceListView(BaseListView):
    model = PriceMatrix
    template_name = "admin/productprice/product_price_list.html"

    def get_breadcumb(self, request):
        return [

        ]

    def get_ttab_name(self):
        return "productprice"

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
        return "Product Price List | BDReads.com"


class AdminProductPriceCreateView(BRBaseCreateView):
    form_class =AdminProductPriceForm
    template_name = "admin/productprice/admin_product_price_create.html"

    def get_form_title(self):
        return "Product Price Create"

    def get_success_url(self):
        return reverse("admin_product_price_list_view")

    def get_cancel_url(self):
        return reverse("admin_product_price_list_view")

    def get_page_title(self):
        return "Create Product Price | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_product_price_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % PriceMatrix.__name__
        }

    def get_context_data(self, **kwargs):
        context = super(AdminProductPriceCreateView, self).get_context_data(**kwargs)
        AdminRentPlanRelationFormSet = formset_factory(AdminRentPlanRelationForm,
                                                       formset=AdminRentPlanFormSet)
        initial = [{"rent_plan": rent_plan_instance.name} for rent_plan_instance in RentPlan.objects.all()]
        context["rent_plan_forms"] = AdminRentPlanRelationFormSet(initial=initial)
        return context
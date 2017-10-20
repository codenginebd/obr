from django.forms.formsets import formset_factory
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib import messages

from bradmin.forms.admin_product_price_forms import AdminProductPriceForm
from bradmin.forms.admin_rent_plan_relation_forms import AdminRentPlanRelationForm, AdminRentPlanFormSet
from bradmin.views.base_create_view import BRBaseCreateView
from bradmin.views.base_list_view import BaseListView
from bradmin.views.base_update_view import BRBaseUpdateView
from ecommerce.models.rent_plan import RentPlan
from ecommerce.models.sales.price_matrix import PriceMatrix
from ecommerce.models.sales.rent_plan_relation import RentPlanRelation
from engine.clock.Clock import Clock
from generics.libs.utils import get_tz_from_request


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
                                                       formset=AdminRentPlanFormSet, max_num=RentPlan.objects.count())
        initial = [{"rent_plan": rent_plan_instance.pk} for rent_plan_instance in RentPlan.objects.all()]
        context["form"] = self.form_class(request=self.request)
        context["rent_plan_forms"] = AdminRentPlanRelationFormSet(initial=initial)
        return context

    def post(self, request, *args, **kwargs):
        price_matrix_form = AdminProductPriceForm(request.POST)
        AdminRentPlanRelationFormSet = formset_factory(AdminRentPlanRelationForm,
                                                       formset=AdminRentPlanFormSet, max_num=RentPlan.objects.count())
        if price_matrix_form.is_valid():
            if price_matrix_form.cleaned_data.get("is_rent"):
                rent_plan_formset = AdminRentPlanRelationFormSet(request.POST, form_kwargs={'request': self.request})
                if rent_plan_formset.is_valid():
                    price_matrix_instance = price_matrix_form.save()
                    for rent_plan_form in rent_plan_formset.forms:
                        rent_plan_relation_instance = rent_plan_form.save(price_matrix_instance=price_matrix_instance)
                    messages.add_message(request=self.request, level=messages.INFO,
                                         message="Created Successfully")
                else:
                    messages.add_message(request=self.request, level=messages.INFO,
                                         message="Form Validation Failed")
            else:
                price_matrix_instance = price_matrix_form.save()
                messages.add_message(request=self.request, level=messages.INFO,
                                     message="Created Successfully")
        return HttpResponseRedirect(self.get_success_url())


class AdminProductPriceUpdateView(BRBaseUpdateView):
    form_class = AdminProductPriceForm
    queryset = PriceMatrix.objects.all()
    template_name = "admin/productprice/admin_product_price_create.html"

    def get_form_title(self):
        return "Product Price Update(#%s)" % self.object.pk

    def get_success_url(self):
        return reverse("admin_product_price_list_view")

    def get_cancel_url(self):
        return reverse("admin_product_price_list_view")

    def get_page_title(self):
        return "Update Product Price | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_product_price_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % PriceMatrix.__name__
        }

    def get_context_data(self, **kwargs):
        context = super(AdminProductPriceUpdateView, self).get_context_data(**kwargs)
        form_count = RentPlan.objects.count()
        AdminRentPlanRelationFormSet = formset_factory(AdminRentPlanRelationForm,
                                                       formset=AdminRentPlanFormSet, max_num=form_count)
        rent_plan_ids = RentPlan.objects.values_list('pk', flat=True)
        rent_plan_objects = RentPlan.objects.all()
        rent_plan_relation_objects = RentPlanRelation.objects.filter(price_matrix_id=self.object.pk, plan_id__in=rent_plan_ids)
        rent_plan_relation_object_dict = {}
        for rent_plan_relation_object in rent_plan_relation_objects:
            rent_plan_relation_object_dict[rent_plan_relation_object.plan.pk] = rent_plan_relation_object
        initial = [{"rent_plan": rent_plan_id} for rent_plan_id in rent_plan_ids ]
        data = {
            'form-TOTAL_FORMS': '%s' % form_count,
            'form-INITIAL_FORMS': '%s' % form_count,
            'form-MAX_NUM_FORMS': '%s' % form_count,
        }

        for index, rent_plan_object in enumerate(rent_plan_objects):
            if rent_plan_relation_object_dict.get(rent_plan_object.pk):
                data["form-%s-price_matrix" % index] = self.object
                data["form-%s-plan" % index] = rent_plan_object
                data["form-%s-rent_rate" % index] = rent_plan_relation_object_dict[rent_plan_object.pk].rent_rate
                data["form-%s-is_special_offer" % index] = rent_plan_relation_object_dict[rent_plan_object.pk].is_special_offer
                data["form-%s-special_rate" % index] = rent_plan_relation_object_dict[rent_plan_object.pk].special_rate
                start_time = rent_plan_relation_object_dict[rent_plan_object.pk].start_time
                if start_time:
                    start_time = Clock.convert_utc_timestamp_to_local_datetime(start_time,
                                                                           get_tz_from_request(self.request))
                else:
                    start_time = ""
                data["form-%s-start_date" % index] = start_time.date().strftime("%m/%d/%Y") if start_time else ""
                end_time = rent_plan_relation_object_dict[rent_plan_object.pk].end_time
                if end_time:
                    end_time = Clock.convert_utc_timestamp_to_local_datetime(end_time,
                                                                         get_tz_from_request(self.request))
                else:
                    end_time = ""
                data["form-%s-end_date" % index] = end_time.date().strftime("%m/%d/%Y") if end_time else ""
        context["rent_plan_forms"] = AdminRentPlanRelationFormSet(initial=initial, data=data)
        return context

    def post(self, request, *args, **kwargs):
        price_matrix_form = AdminProductPriceForm(request.POST, pk=kwargs.get('pk'))
        AdminRentPlanRelationFormSet = formset_factory(AdminRentPlanRelationForm,
                                                       formset=AdminRentPlanFormSet, max_num=RentPlan.objects.count())
        if price_matrix_form.is_valid():
            if price_matrix_form.cleaned_data.get("is_rent"):
                rent_plan_formset = AdminRentPlanRelationFormSet(request.POST, form_kwargs={'request': self.request})
                if rent_plan_formset.is_valid():
                    price_matrix_instance = price_matrix_form.save()
                    for rent_plan_form in rent_plan_formset.forms:
                        rent_plan_relation_instance = rent_plan_form.save(price_matrix_instance=price_matrix_instance)
                    messages.add_message(request=self.request, level=messages.INFO,
                                         message="Updated Successfully")
                else:
                    messages.add_message(request=self.request, level=messages.INFO,
                                         message="Form Validation Failed")
            else:
                price_matrix_instance = price_matrix_form.save()
                rent_plan_relation_instances = RentPlanRelation.objects.filter(price_matrix_id=price_matrix_instance.pk,
                                                                               plan_id__in=RentPlan.objects.values_list('pk', flat=True))
                rent_plan_relation_instances.delete()
                messages.add_message(request=self.request, level=messages.INFO,
                                     message="Updated Successfully")
        return HttpResponseRedirect(self.get_success_url())
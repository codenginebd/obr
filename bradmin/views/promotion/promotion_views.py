from django.forms.formsets import formset_factory
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib import messages
from bradmin.forms.admin_promotion_forms import AdminPromotionForm
from bradmin.forms.admin_promotion_reward_forms import AdminPromotionRewardForm
from bradmin.forms.admin_promotion_reward_product_forms import AdminPromotionRewardProductForm
from bradmin.forms.admin_promotion_rule_forms import AdminPromotionRuleForm
from bradmin.views.base_create_view import BRBaseCreateView
from bradmin.views.base_list_view import BaseListView
from bradmin.views.base_update_view import BRBaseUpdateView
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

    def get_context_data(self, **kwargs):
        context = super(AdminPromotionCreateView, self).get_context_data(**kwargs)
        AdminPromotionRuleFormSet = formset_factory(AdminPromotionRuleForm, max_num=20)
        AdminPromotionRewardFormSet = formset_factory(AdminPromotionRewardForm, max_num=20)
        AdminPromotionRewardProductFormSet = formset_factory(AdminPromotionRewardProductForm, max_num=20)

        context["rule_formset"] = AdminPromotionRuleFormSet(prefix="rule-form")
        context["reward_formset"] = AdminPromotionRewardFormSet(prefix="reward-form")
        context["reward_product_formset_dict"] = {0: AdminPromotionRewardProductFormSet(prefix="reward-product-form-0")}

        return context
        
    def post(self, request, *args, **kwargs):
        
        AdminPromotionRuleFormSet = formset_factory(AdminPromotionRuleForm,max_num=20)
        AdminPromotionRewardFormSet = formset_factory(AdminPromotionRewardForm, max_num=20)
        AdminPromotionRewardProductFormSet = formset_factory(AdminPromotionRewardProductForm, max_num=20)
        
        promotion_form = AdminPromotionForm(request.POST)
        promotion_rule_formset = AdminPromotionRuleFormSet(request.POST, prefix="rule-form", form_kwargs={'request': self.request})
        promotion_reward_formset = AdminPromotionRewardFormSet(request.POST, prefix="reward-form", form_kwargs={'request': self.request})
        promotion_reward_product_formset_dict = { i: AdminPromotionRewardProductFormSet(request.POST, prefix="reward-product-form-%s" % i, form_kwargs={'request': self.request, 'reward_form_prefix': 'reward-form'}) for i in range(0, len(promotion_reward_formset.forms))}

        promotion_form_valid = promotion_form.is_valid()
        promotion_rule_formset_valid = promotion_rule_formset.is_valid()
        promotion_reward_formset_valid = promotion_reward_formset.is_valid()
        if promotion_form_valid and promotion_rule_formset_valid and promotion_reward_formset_valid:
            if all([promotion_reward_product_formset.is_valid() for index, promotion_reward_product_formset in promotion_reward_product_formset_dict.items()]):
                
                promotion_instance = promotion_form.save()
                for product_rule_form in promotion_rule_formset.forms:
                    promotion_product_rule_instance = product_rule_form.save()
                    if promotion_product_rule_instance:
                        promotion_instance.product_rules.add(promotion_product_rule_instance)
                
                promotion_reward_instances = []
                for index, promotion_reward_form in enumerate(promotion_reward_formset.forms):
                    promotion_reward_instance = promotion_reward_form.save()
                    promotion_reward_instances += [promotion_reward_instance]
                    
                    promotion_reward_product_instances = []
                    promotion_reward_product_formset = promotion_reward_product_formset_dict.get(index)
                    if promotion_reward_product_formset:
                        for promotion_reward_product_form in promotion_reward_product_formset.forms:
                            promotion_reward_product_instance = promotion_reward_product_form.save()
                            promotion_reward_product_instances += [promotion_reward_product_instance]
                    promotion_reward_instance.products.add(*promotion_reward_product_instances)
                promotion_instance.rewards.add(*promotion_reward_instances)
                messages.add_message(request=self.request, level=messages.INFO,
                                         message="Created Successfully")
            else:
                messages.add_message(request=self.request, level=messages.INFO,
                                         message="Form Validation Failed")
        else:
            messages.add_message(request=self.request, level=messages.INFO,
                                         message="Form Validation Failed")
        return HttpResponseRedirect(self.get_success_url())
        
        
class AdminPromotionUpdateView(BRBaseUpdateView):
    form_class =AdminPromotionForm
    queryset = Promotion.objects.all()
    template_name = "admin/promotion/admin_promotion_create.html"

    def get_form_title(self):
        return "Promotion Update(#%s)" % self.object.pk

    def get_success_url(self):
        return reverse("admin_promotion_list_view")

    def get_cancel_url(self):
        return reverse("admin_promotion_list_view")

    def get_page_title(self):
        return "Update Promotion | BDReads.com"

    def get_left_menu_items(self):
        return {
            "All": reverse("admin_promotion_list_view"),
            "Error Logs": reverse("admin_error_logs_view") + "?context=%s" % Promotion.__name__
        }

    def get_context_data(self, **kwargs):
        context = super(AdminPromotionUpdateView, self).get_context_data(**kwargs)
        
        AdminPromotionProductRuleFormSet = formset_factory(AdminPromotionRuleForm, max_num=20)
        AdminPromotionRewardFormSet = formset_factory(AdminPromotionRewardForm, max_num=20)
        AdminPromotionRewardProductFormSet = formset_factory(AdminPromotionRewardProductForm, max_num=20)
        
        # Data initialization
        product_rules_object_count = self.object.product_rules.count()
        product_rule_data = {
            'rule-form-TOTAL_FORMS': '%s' % product_rules_object_count,
            'rule-form-INITIAL_FORMS': '%s' % product_rules_object_count,
            'rule-form-MAX_NUM_FORMS': '20',
        }
        product_rules_objects = self.object.product_rules.all()
        for index, product_rule_object in enumerate(product_rules_objects):
            product_rule_data["rule-form-%s-rule_id"] = product_rule_object.pk
            product_rule_data["rule-form-%s-rule_product"] = product_rule_object.get_product_instance()
            product_rule_data["rule-form-%s-rule_is_new"] = product_rule_object.is_new
            product_rule_data["rule-form-%s-rule_print_type"] = product_rule_object.print_type
            product_rule_data["rule-form-%s-min_qty"] = product_rule_object.min_qty
            product_rule_data["rule-form-%s-min_amount"] = product_rule_object.min_amount
            
        context["rule_formset"] = AdminPromotionProductRuleFormSet(data=product_rule_data)
        
        promotion_reward_object_count = self.rewards.count()
        promotion_reward_data = {
            'reward-form-TOTAL_FORMS': '%s' % promotion_reward_object_count,
            'reward-form-INITIAL_FORMS': '%s' % promotion_reward_object_count,
            'reward-form-MAX_NUM_FORMS': '%s' % 20,
        }
        
        promotion_reward_formsets = {}
        promotion_reward_product_formsets = {}
        
        promotion_reward_objects = self.rewards.all()
        for index, promotion_reward_object in enumerate(promotion_reward_objects):
            promotion_reward_data["reward-form-%-reward_id"] = promotion_reward_object.pk
            promotion_reward_data["reward-form-%-reward_type"] = promotion_reward_object.reward_type
            promotion_reward_data["reward-form-%-gift_amount"] = promotion_reward_object.gift_amount
            promotion_reward_data["reward-form-%-gift_amount_in_percentage"] = promotion_reward_object.gift_amount_in_percentage
            promotion_reward_data["reward-form-%-store_credit"] = promotion_reward_object.store_credit
            promotion_reward_data["reward-form-%-credit_expiry_time"] = promotion_reward_object.credit_expiry_time
            
            promotion_reward_product_count = promotion_reward_object.products.count()
            promotion_reward_product_data = {
                'reward-product-form-%s-TOTAL_FORMS' % index: '%s' % promotion_reward_product_count,
                'reward-product-form-%s-INITIAL_FORMS' % index: '%s' % promotion_reward_product_count,
                'reward-product-form-%s-MAX_NUM_FORMS' % index: '%s' % 20,
            }
            promotion_reward_products = promotion_reward_object.products.all()
            for index2, promotion_reward_product in enumerate(promotion_reward_products):
                promotion_reward_product_data['reward-product-form-%s-%s-reward_product_id' % (index, index2)] = promotion_reward_product.pk
                promotion_reward_product_data['reward-product-form-%s-%s-reward_product' % (index, index2)] = promotion_reward_product.get_product_instance()
                promotion_reward_product_data['reward-product-form-%s-%s-reward_is_new' % (index, index2)] = promotion_reward_product.is_new
                promotion_reward_product_data['reward-product-form-%s-%s-reward_print_type' % (index, index2)] = promotion_reward_product.print_type
                promotion_reward_product_data['reward-product-form-%s-%s-quantity' % (index, index2)] = promotion_reward_product.quantity
            promotion_reward_product_formsets[index] = AdminPromotionRewardProductFormSet(data=promotion_reward_product_data)
            
        context["reward_formset"] = AdminPromotionRewardFormSet(data=promotion_reward_data)
        context["reward_product_formset_dict"] = promotion_reward_product_formsets
        
        return context
        
    def post(self, request, *args, **kwargs):
        
        AdminPromotionRuleFormSet = formset_factory(AdminPromotionRuleForm,max_num=20)
        AdminPromotionRewardFormSet = formset_factory(AdminPromotionRewardForm, max_num=20)
        AdminPromotionRewardProductFormSet = formset_factory(AdminPromotionRewardProductForm, max_num=20)
        
        promotion_form = AdminPromotionForm(request.POST)
        promotion_rule_formset = AdminPromotionRuleFormSet(request.POST, prefix="rule-form", form_kwargs={'request': self.request})
        promotion_reward_formset = AdminPromotionRewardFormSet(request.POST, prefix="reward-form", form_kwargs={'request': self.request})
        promotion_reward_product_formset_dict = {}
        
        if promotion_form.is_valid() and promotion_rule_formset.is_valid() and promotion_reward_formset.is_valid():
            for index, promotion_reward_form in enumerate(promotion_reward_formset.forms):
                 promotion_reward_product_formset = AdminPromotionRewardProductFormSet(request.POST, prefix="reward-product-form-%s" % index, form_kwargs={'request': self.request, 'reward_form_prefix': 'reward-form-%s' % index})
                 if not promotion_reward_product_formset.is_valid():
                    messages.add_message(request=self.request, level=messages.INFO,
                                         message="Form Validation Failed")
                    return HttpResponseRedirect(self.get_success_url())
                
            promotion_instance = promotion_form.save()
            for product_rule_form in promotion_rule_formset.forms:
                promotion_product_rule_instance = product_rule_form.save()
                if promotion_product_rule_instance:
                    promotion_instance.product_rules.add(promotion_product_rule_instance)
                
            promotion_reward_instances = []
            for index, promotion_reward_form in enumerate(promotion_reward_formset.forms):
                promotion_reward_instance = promotion_reward_form.save()
                promotion_reward_instances += [promotion_reward_instance]
                    
                promotion_reward_product_instances = []
                promotion_reward_product_formset = promotion_reward_product_formset_dict.get(index)
                if promotion_reward_product_formset:
                    for promotion_reward_product_form in promotion_reward_product_formset.forms:
                        promotion_reward_product_instance = promotion_reward_product_form.save()
                        if promotion_reward_product_instance:
                            promotion_reward_product_instances += [promotion_reward_product_instance]
                promotion_reward_instance.products.add(*promotion_reward_product_instances)
            promotion_instance.rewards.add(*promotion_reward_instances)
            messages.add_message(request=self.request, level=messages.INFO,
                                         message="Updated Successfully")
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(request=self.request, level=messages.INFO,
                                         message="Form Validation Failed")
            return HttpResponseRedirect(self.get_success_url())

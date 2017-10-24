from decimal import Decimal
from django import forms
from book_rental.models.sales.book import Book
from bradmin.forms.base_model_form import BRBaseModelForm
from bradmin.forms.fields.product_model_choice_field import ProductModelChoiceField
from promotion.models.promotion_products_rule import PromotionProductRule


class AdminPromotionRuleForm(BRBaseModelForm):

    id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    rule_product = ProductModelChoiceField(label="Select Product",
                                      queryset=Book.objects.all(),
                                      widget=forms.Select(attrs={"class": "form-control"}))

    rule_is_new = forms.BooleanField(label="Is New")

    rule_print_type = forms.ChoiceField(label="Printing Type",
                                   choices=(("ECO", "Economy"), ("COL", "Color"), ("ORI", "Original")),
                                   widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(AdminPromotionRuleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PromotionProductRule
        fields = ['id', 'rule_product', 'rule_is_new', 'rule_print_type', 'min_qty', 'min_amount']
        
    def is_valid(self):
        self.error_messages = []
        self.cleaned_data = {}
        prefix = self.prefix
        id = self.data.get(prefix + "-id")
        product = self.data.get(prefix + "-rule_product")
        is_new = self.data.get(prefix + "-rule_is_new")
        print_type = self.data.get(prefix + "-rule_print_type")
        min_qty = self.data.get(prefix + "-min_qty")
        min_amount = self.data.get(prefix + "-min_amount")
        by_cart_choice = self.data.get("by_cart_choice")
        by_amount_choice = self.data.get("by_amount_choice")
        if by_cart_choice == "by_products":
            if not product or is_new is None or not print_type:
                self.error_messages += [ "Product information missing in the rule" ]
                return False
            if by_amount_choice == "by_amount":
                if not min_amount:
                    self.error_messages += [ "Product rule Min Amount is required" ]
                    return False
                try:
                    min_amount = Decimal(min_amount)
                except:
                    self.error_messages += [ "A valid product rule Min Amount is required" ]
                    return False
            if by_amount_choice == "by_qty":
                if not min_qty:
                    self.error_messages += [ "Product rule Min Qty is required" ]
                    return False
                try:
                    min_qty = Decimal(min_qty)
                except:
                    self.error_messages += [ "A valid product rule Min Qty is required" ]
                    return False
            if id:
                try:
                    id = int(id)
                except:
                    self.error_messages += [ "Invalid ID Given" ]
                    return False
        
            is_new = 1 if is_new else 0
        
            self.cleaned_data = {}
            self.cleaned_data["id"] = id
            if product:
                product = Book.objects.get(pk=int(product))
                self.cleaned_data["product"] = product
            if is_new:
                self.cleaned_data["is_new"] = is_new
            if print_type:
                self.cleaned_data["print_type"] = print_type
            if min_qty:
                self.cleaned_data["min_qty"] = min_qty
            if min_amount:
                self.cleaned_data["min_amount"] = min_amount
            return True
        return True
        
    def save(self, **kwargs):
        if self.cleaned_data.get("id"):
            promotion_rule_instance = PromotionProductRule.objects.get(pk=id)
        else:
            promotion_rule_instance = PromotionProductRule()
        if self.cleaned_data.get('product'):
            promotion_rule_instance.product_id = self.cleaned_data['product'].pk
            promotion_rule_instance.product_model = self.cleaned_data['product'].__class__.__name__
            promotion_rule_instance.save()
    

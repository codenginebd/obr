from decimal import Decimal
from django import forms
from book_rental.models.sales.book import Book
from bradmin.forms.base_model_form import BRBaseModelForm
from bradmin.forms.fields.product_model_choice_field import ProductModelChoiceField
from promotion.models.promotion_products_rule import PromotionProductRule


class AdminPromotionRuleForm(BRBaseModelForm):

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
        fields = ['rule_product', 'rule_is_new', 'rule_print_type', 'min_qty', 'min_amount']
        
    def is_valid(self):
        self.error_messages = []
        self.cleaned_data = {}
        prefix = self.prefix
        product = self.data.get(prefix + "-rule_product")
        is_new = self.data.get(prefix + "-rule_is_new")
        print_type = self.data.get(prefix + "-rule_print_type")
        min_qty = self.data.get(prefix + "-min_qty")
        min_amount = self.data.get(prefix + "-min_amount")
        by_cart_choice = self.data.get("by_cart_choice")
        by_amount_choice = self.data.get("by_amount_choice")
        if by_cart_choice == "by_products":
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
        
        is_new = 1 if is_new else 0
        product = Book.objects.get(pk=int(product))
        self.cleaned_data = {}
        self.cleaned_data["product"] = product
        self.cleaned_data["is_new"] = is_new
        self.cleaned_data["print_type"] = print_type
        self.cleaned_data["min_qty"] = min_qty
        self.cleaned_data["min_amount"] = min_amount
        return True

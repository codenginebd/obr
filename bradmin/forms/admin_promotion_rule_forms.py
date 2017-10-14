from django import forms
from book_rental.models.sales.book import Book
from bradmin.forms.base_model_form import BRBaseModelForm
from bradmin.forms.fields.product_model_choice_field import ProductModelChoiceField
from promotion.models.promotion_products_rule import PromotionProductRule


class AdminPromotionRuleForm(BRBaseModelForm):

    product = ProductModelChoiceField(label="Select Product",
                                      queryset=Book.objects.all())

    print_type = forms.ChoiceField(label="Printing Type",
                                   choices=(("ECO", "Economy"), ("COL", "Color"), ("ORI", "Original")),
                                   widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(AdminPromotionRuleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PromotionProductRule
        fields = ['product', 'is_new', 'print_type', 'min_qty', 'min_amount']
        widgets = {

        }
        labels = {
        }



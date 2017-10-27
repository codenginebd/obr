from django import forms
from book_rental.models.sales.book import Book
from bradmin.forms.base_model_form import BRBaseModelForm
from bradmin.forms.fields.product_model_choice_field import ProductModelChoiceField
from promotion.models.promotion_reward_products import PromotionRewardProduct


class AdminPromotionRewardProductForm(BRBaseModelForm):

    reward_product_id = forms.IntegerField(widget=forms.HiddenInput())

    reward_product = ProductModelChoiceField(label="Select Product",
                                      queryset=Book.objects.all(),
                                      widget=forms.Select(attrs={"class": "form-control"}))

    reward_is_new = forms.BooleanField(label="Is New")

    reward_print_type = forms.ChoiceField(label="Printing Type",
                                   choices=(("ECO", "Economy"), ("COL", "Color"), ("ORI", "Original")),
                                   widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(AdminPromotionRewardProductForm, self).__init__(*args, **kwargs)
        self.fields["quantity"].widget.attrs["class"] = "form-control"

    class Meta:
        model = PromotionRewardProduct
        fields = ['reward_product_id', 'reward_product', 'reward_is_new', 'reward_print_type', 'quantity']
        
    


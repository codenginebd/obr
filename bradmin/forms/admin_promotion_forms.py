from django import forms
from bradmin.forms.base_model_form import BRBaseModelForm
from bradmin.forms.fields.currency_model_choice_field import CurrencyModelChoiceField
from enums import PromotionTypes
from payment.models.currency import Currency
from promotion.models.promotion import Promotion

promo_type_choices = (
    (PromotionTypes.BUY.value, "Buy"),
    (PromotionTypes.RENT.value, "Rent"),
    (PromotionTypes.ANY.value, "Any"))


class AdminPromotionForm(BRBaseModelForm):

    promotion_type = forms.ChoiceField(choices=promo_type_choices,
                                       widget=forms.Select(attrs={"class": "form-control"}))

    BY_CART_CHOICES = (
        ("by_cart", 'By Cart'),
        ("by_product", 'By Product'),
        ("by_date", "By Date")
    )
    by_cart_choice = forms.ChoiceField(choices=BY_CART_CHOICES,
                                            widget=forms.RadioSelect(attrs={"class": "list-inline"}))

    BY_amount_CHOICES = (
        ("by_amount", 'By Amount'),
        ("by_quantity", 'By Quantity')
    )
    by_amount_choice = forms.ChoiceField(choices=BY_amount_CHOICES,
                                       widget=forms.RadioSelect(attrs={"class": "list-inline"}))

    currency = CurrencyModelChoiceField(label="Select Currency", queryset=Currency.objects.all(),
                                        widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(AdminPromotionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Promotion
        fields = ['title', 'description', 'promotion_type', 'by_cart_choice',
                  'by_amount_choice', 'currency', 'min_qty', 'min_amount', 'start_date', 'end_date']
        widgets = {

        }
        labels = {
        }



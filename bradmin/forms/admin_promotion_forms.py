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

    by_cart_hidden = forms.CharField(widget=forms.HiddenInput())
    by_amount_hidden = forms.CharField(widget=forms.HiddenInput())

    currency = CurrencyModelChoiceField(label="Select Currency", queryset=Currency.objects.all(),
                                        widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(AdminPromotionForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["class"] = "form-control"
        self.fields["description"].widget.attrs["class"] = "form-control"
        self.fields["promotion_type"].widget.attrs["class"] = "form-control"
        self.fields["currency"].widget.attrs["class"] = "form-control"
        self.fields["currency"].empty_label = None
        self.fields["min_qty"].widget.attrs["class"] = "form-control"
        self.fields["min_amount"].widget.attrs["class"] = "form-control"
        self.fields["start_date"].widget.attrs["class"] = "form-control"
        self.fields["end_date"].widget.attrs["class"] = "form-control"

    class Meta:
        model = Promotion
        fields = ['title', 'description', 'promotion_type', 'currency', 'min_qty',
                  'min_amount', 'start_date', 'end_date']
        widgets = {

        }
        labels = {
        }



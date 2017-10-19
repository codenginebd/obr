from django import forms
from django.forms.formsets import formset_factory
from book_rental.models.sales.book import Book
from bradmin.forms.base_model_form import BRBaseModelForm
from bradmin.forms.fields.currency_model_choice_field import CurrencyModelChoiceField
from bradmin.forms.fields.product_model_choice_field import ProductModelChoiceField
from ecommerce.models.sales.price_matrix import PriceMatrix
from payment.models.currency import Currency


class AdminProductPriceForm(BRBaseModelForm):

    product = ProductModelChoiceField(label="Select Product",
                                      queryset=Book.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    print_type = forms.ChoiceField(label="Printing Type",
                                   choices=(("ECO", "Economy"), ("COL", "Color"), ("ORI", "Original")),
                                   widget=forms.Select(attrs={"class": "form-control"}))

    currency = CurrencyModelChoiceField(label="Select Currency", queryset=Currency.objects.all(),
                                        widget=forms.Select(attrs={"class": "form-control"}))

    is_new = forms.ChoiceField(label="Is New",
                                   choices=(("1", "Yes"), ("0", "No")),
                                   widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(AdminProductPriceForm, self).__init__(*args, **kwargs)
        self.fields["base_price"].widget.attrs["class"] = "form-control"
        self.fields["market_price"].widget.attrs["class"] = "form-control"
        self.fields["sale_price"].widget.attrs["class"] = "form-control"
        self.fields["initial_payable_rent_price"].widget.attrs["class"] = "form-control"
        self.fields["offer_price_p"].widget.attrs["class"] = "form-control"
        self.fields["offer_price_v"].widget.attrs["class"] = "form-control"
        self.fields["offer_date_start"].widget.attrs["class"] = "form-control"
        self.fields["offer_date_end"].widget.attrs["class"] = "form-control"
        self.fields["product"].empty_label = None
        self.fields["currency"].empty_label = None

    class Meta:
        model = PriceMatrix
        fields = ['product', "is_new", "print_type", "base_price", "market_price", "sale_price", "is_rent",
                  "initial_payable_rent_price", "custom_rent_plan_available", "currency", "offer_date_start", "offer_date_end",
                  "special_price", "offer_price_p", "offer_price_v","is_rent"]

        labels = {
            "offer_price_p": "Offer Price(%)",
            "offer_price_v": "Offer Price(Value)",
            "is_rent": "Is Rent Available"
        }

        widgets = {
            "offer_date_start": forms.DateInput(),
            "offer_date_end": forms.DateInput()
        }



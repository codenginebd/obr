from django import forms
from book_rental.models.sales.book import Book
from bradmin.forms.base_model_form import BRBaseModelForm
from bradmin.forms.fields.currency_model_choice_field import CurrencyModelChoiceField
from bradmin.forms.fields.product_model_choice_field import ProductModelChoiceField
from ecommerce.models.sales.price_matrix import PriceMatrix
from payment.models.currency import Currency


class AdminProductPriceForm(BRBaseModelForm):

    product = ProductModelChoiceField(label="Select Book",
                                      queryset=Book.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    print_type = forms.ChoiceField(label="Printing Type",
                                   choices=(("ECO", "Economy"), ("COL", "Color"), ("ORI", "Original")),
                                   widget=forms.Select(attrs={"class": "form-control"}))

    currency = CurrencyModelChoiceField(label="Select Currency", queryset=Currency.objects.all(),
                                        widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(AdminProductPriceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PriceMatrix
        fields = ['product', "is_new", "print_type", "base_price", "market_price", "sale_price",
                  "initial_payable_rent_price", "currency", "offer_date_start", "offer_date_end",
                  "special_price", "offer_price_p", "offer_price_v","is_rent"]
        widgets = {
                "is_new": forms.CheckboxInput(attrs={"class": "form-control"})
        }
        labels = {

        }



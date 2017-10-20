from datetime import datetime
from decimal import Decimal
from django import forms
from django.forms.formsets import formset_factory
from book_rental.models.sales.book import Book
from bradmin.forms.base_model_form import BRBaseModelForm
from bradmin.forms.fields.currency_model_choice_field import CurrencyModelChoiceField
from bradmin.forms.fields.product_model_choice_field import ProductModelChoiceField
from ecommerce.models.sales.price_matrix import PriceMatrix
from engine.clock.Clock import Clock
from generics.libs.loader.loader import load_model
from generics.libs.utils import get_tz_from_request
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
        if kwargs.get("instance"):
            instance = kwargs.get("instance")
            if instance.is_new:
                self.fields["is_new"].initial = "1"
            else:
                self.fields["is_new"].initial = "0"

            if instance.special_price:
                special_offer_start = Clock.convert_utc_timestamt_to_local_datetime(instance.offer_start_date, get_tz_from_request(self.request))
                special_offer_end = Clock.convert_utc_timestamt_to_local_datetime(instance.offer_date_end,
                                                                                    get_tz_from_request(self.request))
                self.fields["offer_date_start"].initial = special_offer_start
                self.fields["offer_date_end"].initial = special_offer_end

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

    def is_valid(self):
        product = self.data["product"]
        is_new = self.data["is_new"]
        print_type = self.data["print_type"]
        base_price = self.data["base_price"]
        market_price = self.data["market_price"]
        sale_price = self.data["sale_price"]
        currency = self.data["currency"]

        if any([not base_price, not market_price, not sale_price]):
            return False

        Book = load_model(app_label="book_rental", model_name="Book")
        product = Book.objects.get(pk=int(product))
        currency = Currency.objects.get(pk=int(currency))
        is_new = 0 if not is_new else 1
        is_new = bool(is_new)

        try:
            base_price = Decimal(base_price)
        except:
            return False

        try:
            market_price = Decimal(market_price)
        except:
            return False

        try:
            sale_price = Decimal(sale_price)
        except:
            return False

        special_price = self.data.get("special_price")
        offer_price_p = self.data.get("offer_price_p")
        offer_price_v = self.data.get("offer_price_v")
        offer_date_start = self.data.get("offer_date_start")
        offer_date_end = self.data.get("offer_date_end")
        special_price = 0 if not special_price else 1
        special_price = bool(special_price)
        if special_price:
            if any([not offer_price_p, not offer_price_v, not offer_date_start, not offer_date_end]):
                return False

            try:
                offer_price_p = Decimal(offer_price_p)
            except:
                return False

            try:
                offer_price_v = Decimal(offer_price_v)
            except:
                return False

            try:
                offer_date_start = datetime.strptime(offer_date_start, "%m/%d/%Y")
                offer_date_end = datetime.strptime(offer_date_end, "%m/%d/%Y")
            except:
                return False

        is_rent = self.data.get("is_rent")
        initial_payable_rent_price = self.data.get("initial_payable_rent_price")
        custom_rent_plan_available = self.data.get("custom_rent_plan_available")

        is_rent = 0 if not is_rent else 1
        is_rent = bool(is_rent)
        custom_rent_plan_available = 0 if not custom_rent_plan_available else 1
        custom_rent_plan_available = bool(custom_rent_plan_available)
        if is_rent:
            if not initial_payable_rent_price:
                return False
            initial_payable_rent_price = Decimal(initial_payable_rent_price)

        self.cleaned_data = {}

        self.cleaned_data["product"] = product
        self.cleaned_data["is_new"] = is_new
        self.cleaned_data["print_type"] = print_type
        self.cleaned_data["base_price"] = base_price
        self.cleaned_data["market_price"] = market_price
        self.cleaned_data["sale_price"] = sale_price
        self.cleaned_data["currency"] = currency
        self.cleaned_data["special_price"] = special_price
        if special_price:
            self.cleaned_data["offer_price_p"] = offer_price_p
            self.cleaned_data["offer_price_v"] = offer_price_v
            self.cleaned_data["offer_date_start"] = Clock.convert_datetime_to_utc_timestamp(offer_date_start)
            self.cleaned_data["offer_date_end"] = Clock.convert_datetime_to_utc_timestamp(offer_date_end)

        if is_rent:
            self.cleaned_data["is_rent"] = is_rent
            self.cleaned_data["initial_payable_rent_price"] = initial_payable_rent_price
            self.cleaned_data["custom_rent_plan_available"] = custom_rent_plan_available

        return True

    def save(self, commit=True):
        if not self.instance:
            self.instance = PriceMatrix()

        self.instance.product_code = self.cleaned_data["product"].code
        self.instance.product_model = self.cleaned_data["product"].__class__.__name__
        self.instance.is_new = self.cleaned_data["is_new"]
        self.instance.print_type = self.cleaned_data["print_type"]
        self.instance.base_price = self.cleaned_data["base_price"]
        self.instance.market_price = self.cleaned_data["market_price"]
        self.instance.sale_price = self.cleaned_data["sale_price"]
        self.instance.currency_id = self.cleaned_data["currency"].pk

        self.instance.special_price = self.cleaned_data["special_price"]
        if self.instance.special_price:
            self.instance.offer_price_p = self.cleaned_data["offer_price_p"]
            self.instance.offer_price_v = self.cleaned_data["offer_price_v"]
            self.instance.offer_date_start = self.cleaned_data["offer_date_start"]
            self.instance.offer_date_end = self.cleaned_data["offer_date_end"]
        else:
            self.instance.offer_price_p = None
            self.instance.offer_price_v = None
            self.instance.offer_date_start = None
            self.instance.offer_date_end = None

        self.instance.is_rent = self.cleaned_data["is_rent"]
        if self.instance.is_rent:
            self.instance.initial_payable_rent_price = self.cleaned_data["initial_payable_rent_price"]
            self.instance.custom_rent_plan_available = self.cleaned_data["custom_rent_plan_available"]
        else:
            self.instance.initial_payable_rent_price = None
            self.instance.custom_rent_plan_available = None
        self.instance.save()
        return self.instance



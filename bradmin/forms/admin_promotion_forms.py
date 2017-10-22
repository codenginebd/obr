from datetime import datetime
from django import forms
from decimal import Decimal
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

    by_cart_choice = forms.ChoiceField(choices=(("By Cart", "by_cart"), ("By Products", "by_products"), ("By Date", "by_date")),
                                       widget=forms.Select(attrs={"class": "form-control"}))
    by_amount_choice = forms.ChoiceField(choices=("By Amount", "by_amount"), ("By Quantity", "by_quantity")),
                                       widget=forms.Select(attrs={"class": "form-control"}))

    currency = CurrencyModelChoiceField(label="Select Currency", queryset=Currency.objects.all(),
                                        widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        if kwargs.get('pk'):
            self.pk = kwargs.pop('pk')
        else:
            self.pk = None
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
        self.fields["by_cart_choice"].empty_label = None
        self.fields["by_amount_choice"].empty_label = None

    class Meta:
        model = Promotion
        fields = ['title', 'description', 'promotion_type', 'currency', 'by_cart_choice', 'by_amount_choice', 'min_qty',
                  'min_amount', 'start_date', 'end_date']
        widgets = {

        }
        labels = {
        }
        
    def is_valid(self):
        self.errors_messages = []
        self.cleaned_data = {}
        title = self.data.get("title")
        description = self.data.get("description")
        promotion_type = self.data.get("promotion_type")
        currency = self.data.get("currency")
        by_cart_choice = self.data.get("by_cart_choice")
        by_amount_choice = self.data.get("by_amount_choice")
        min_qty = self.data.get("min_qty")
        min_amount = self.data.get("min_amount")
        start_date = self.data.get("start_date")
        end_date = self.data.get("end_date")
        mandatory_list = [ title, description, promotion_type, currency, by_cart_choice, by_amount_choice, start_date, end_date ]
        mandatory_list_name = [ "title", "description", "promotion_type", "currency", "by_cart_choice", "by_amount_choice", "start_date", "end_date" ]
        if any([not field in mandatory_list]):
            self.errors_messages += [" ".join([word.capitalize() for word in field.split("_")]) + " is required" for field in mandatory_list_name if not field ]
            return False
            
        if by_cart_choice == "by_cart" and by_amount_choice == "by_amount":
            if not min_amount:
                self.errors_messages += [ "Min Amount is required" ]
                return False
            
            try:
                min_amount = Decimal(min_amount)
            except:
                self.errors_messages += [ "A Valid Min Amount is required" ]
                return False
                
        elif by_cart_choice == "by_cart" and by_amount_choice == "by_quantity":
            if not min_qty:
                self.errors_messages += [ "Min Qty is required" ]
                return False
            
            try:
                min_qty = int(min_qty)
            except:
                self.errors_messages += [ "A Valid Min Qty is required" ]
                return False
                
        try:
            start_date = datetime.strptime(start_date, "%m/%d/%Y").date()
        except:
            self.errors_messages += [ "Start Date is invalid. Expected format: mm/dd/YYYY" ]
            return False
            
        try:
            end_date = datetime.strptime(end_date, "%m/%d/%Y").date()
        except:
            self.errors_messages += [ "End Date is invalid. Expected format: mm/dd/YYYY" ]
            return False
            
        try:
            currency = int(currency)
        except:
            self.errors_messages += [ "Invalid Currency Id" ]
            return False
            
        # Cleaning Data
        currency = Currency.objects.get(pk=currency)
        
        self.cleaned_data["title"] = title
        self.cleaned_data["description"] = description
        self.cleaned_data["promotion_type"] = promotion_type
        self.cleaned_data["currency"] = currency
        self.cleaned_data["by_cart_choice"] = by_cart_choice
        self.cleaned_data["by_amount_choice"] = by_amount_choice
        self.cleaned_data["min_qty"] = min_qty
        self.cleaned_data["min_amount"] = min_amount
        self.cleaned_data["start_date"] = start_date
        self.cleaned_data["end_date"] = end_date
        
        return True
            
    def save(self, commit=True):
        if self.pk:
            promotion_instance = Promotion.objects.get(pk=self.pk)
        else:
            promotion_instance = Promotion()
            
        promotion_instance.title = self.cleaned_data["title"]
        promotion_instance.description = self.cleaned_data["description"]
        promotion_instance.promotion_type = self.cleaned_data["promotion_type"]
        promotion_instance.currency_id = self.cleaned_data["currency"].pk
        by_cart_choice = self.cleaned_data["by_cart_choice"]
        by_amount_choice = self.cleaned_data["by_amount_choice"]
        if by_cart_choice == "by_cart":
            promotion_instance.by_cart = True
            promotion_instance.by_products = False
            promotion_instance.by_dates = False
        elif by_cart_choice == "by_products":
            promotion_instance.by_cart = False
            promotion_instance.by_products = True
            promotion_instance.by_dates = False
        elif by_cart_choice == "by_date":
            promotion_instance.by_cart = False
            promotion_instance.by_products = False
            promotion_instance.by_dates = True
            
        if by_amount_choice == "by_amount":
            promotion_instance.by_amount = True
            promotion_instance.by_quantity = False
            
        elif by_amount_choice == "by_quantity":
            promotion_instance.by_amount = False
            promotion_instance.by_quantity = True
            
        if self.cleaned_data.get("min_qty"):
            promotion_instance.min_qty = self.cleaned_data["min_qty"]
            
        if self.cleaned_data.get("min_amount"):
            promotion_instance.min_amount = self.cleaned_data["min_amount"]
        
        promotion_instance.start_date = self.cleaned_data["start_date"]
        promotion_instance.end_date = self.cleaned_data["end_date"]
        promotion_instance.save()
        return promotion_instance



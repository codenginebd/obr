from django import forms
from book_rental.models.sales.book import Book
from bradmin.forms.base_model_form import BRBaseModelForm
from bradmin.forms.fields.product_model_choice_field import ProductModelChoiceField
from bradmin.forms.fields.warehouse_model_choice_field import WarehouseModelChoiceField
from ecommerce.models.sales.warehouse import Warehouse
from generics.libs.loader.loader import load_model
from inventory.models.inventory import Inventory


class AdminInventoryForm(BRBaseModelForm):

    warehouse = WarehouseModelChoiceField(label="Select Warehouse",
                                          queryset=Warehouse.objects.all(),
                                          widget=forms.Select(attrs={'class': 'form-control'}))
    product = ProductModelChoiceField(label="Select Book",
                                      queryset=Book.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    print_type = forms.ChoiceField(label="Printing Type",
                                   choices=(("ECO", "Economy"),("COL", "Color"),("ORI", "Original")),
                                   widget=forms.Select(attrs={"class": "form-control"}))

    is_new = forms.ChoiceField(label="Is New",
                                   choices=(("1", "Yes"),("0", "No")),
                                   widget=forms.Select(attrs={"class": "form-control"}))

    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

    stock = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(AdminInventoryForm, self).__init__(*args, **kwargs)
        if kwargs.get("instance"):
            instance = kwargs.get("instance")
            product_id = instance.product_id
            product_model = instance.product_model
            if product_model == "Book":
                Book = load_model(app_label="book_rental", model_name="Book")
                product_instance = Book.objects.get(pk=product_id)
                self.initial["product"] = product_instance

    class Meta:
        model = Inventory
        fields = ['warehouse', 'product', 'is_new', 'print_type', 'stock', 'available_for_buy', 'available_for_rent', 'available_for_sale',
                  'comment']
        widgets = {

        }
        labels = {
            "warehouse": "Select Warehouse",
            "product": "Select Book"
        }

    def clean(self):
        return super(AdminInventoryForm, self).clean()

    def save(self, commit=True):
        warehouse = self.cleaned_data['warehouse']
        product = self.cleaned_data['product']
        product_id = product.pk
        product_model = product.__class__.__name__
        stock = self.cleaned_data['stock']
        is_new = self.cleaned_data['is_new']
        print_type = self.cleaned_data['print_type']
        available_for_buy = self.cleaned_data['available_for_buy']
        available_for_rent = self.cleaned_data['available_for_rent']
        available_for_sale = self.cleaned_data['available_for_sale']
        comment = self.cleaned_data['comment']

        if self.instance.pk:
            instance = self.instance
        else:
            instance = Inventory()
        instance.product_id = product_id
        instance.product_model = product_model
        instance.is_new = is_new
        instance.print_type = print_type
        instance.warehouse_id = warehouse.pk
        instance.stock = stock
        instance.available_for_buy = available_for_buy
        instance.available_for_rent = available_for_rent
        instance.available_for_sale = available_for_sale
        instance.comment = comment
        instance.save()
        return instance



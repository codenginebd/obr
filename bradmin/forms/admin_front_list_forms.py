from django import forms

from book_rental.models.sales.book import Book
from bradmin.forms.base_model_form import BRBaseModelForm
from ecommerce.models.front_list import FrontList
from ecommerce.models.front_list_product import FrontListProduct
from ecommerce.models.sales.category import ProductCategory
from enums import FrontListRule
from generics.libs.loader.loader import load_model


class AdminFrontListForm(BRBaseModelForm):

    front_products = forms.ModelMultipleChoiceField(label="Products",
                                              queryset=Book.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    exclude_front_products = forms.ModelMultipleChoiceField(label="Exclude Products",
                                                    queryset=Book.objects.all(),
                                                    widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    rule_name = forms.ChoiceField(choices=(
        (FrontListRule.TOP_X_PTC_DISCOUNT.value, "Top X Percentage Discount"),
        (FrontListRule.MOST_POPULAR.value, "Most Popular On Category"),
        (FrontListRule.MOST_POPULAR_ALL.value, "Most Popular All"),
        (FrontListRule.BEST_SELLER.value, "Best Seller On Category"),
        (FrontListRule.BEST_SELLER_ALL.value, "Best Seller All"),
        (FrontListRule.TOP_SEARCHED.value, "Top Searched On Category"),
        (FrontListRule.TOP_SEARCHED_ALL.value, "Top Searched All"),
        (FrontListRule.NEW_BOOKS.value, "New Books On Category"),
        (FrontListRule.NEW_BOOKS_ALL.value, "New Books All")
    ),widget=forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}))

    category = forms.ModelChoiceField(label="Select Category",
                                      queryset=ProductCategory.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}))

    def __init__(self, *args, **kwargs):
        super(AdminFrontListForm, self).__init__(*args, **kwargs)
        self.fields['title_2'].required = False
        self.fields['description'].required = False
        self.fields['rule_name'].required = False
        self.fields['category'].required = False
        self.fields['top_limit'].required = False
        self.fields['max_limit'].required = False
        self.fields['front_products'].required = False
        if "instance" in kwargs:
            instance = kwargs["instance"]
            if instance and instance.products.exists():
                product_model = instance.products.first().product_model
                if product_model == "Book":
                    Book = load_model(app_label="book_rental", model_name="Book")
                    fl_products = instance.products.values_list('product_id', flat=True)
                    book_instances = Book.objects.filter(pk__in=fl_products)
                    self.fields['front_products'].initial = book_instances

            if instance and instance.exclude_products.exists():
                product_model = instance.exclude_products.first().product_model
                if product_model == "Book":
                    Book = load_model(app_label="book_rental", model_name="Book")
                    fl_products = instance.exclude_products.values_list('product_id', flat=True)
                    book_instances = Book.objects.filter(pk__in=fl_products)
                    self.fields['exclude_front_products'].initial = book_instances


    class Meta:
        model = FrontList
        fields = ['title', 'title_2', 'show_2', 'description',
                  'by_rule', 'rule_name', 'category', 'top_limit', 'max_limit', 'detail_url', 'palette',
                  'front_products', 'exclude_front_products']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'title_2': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'palette': forms.Select(attrs={'class': 'form-control'}),
            'top_limit': forms.NumberInput(attrs={'class': 'form-control', 'disabled': 'disabled', 'min': '1', 'max': '100'}),
            'max_limit': forms.NumberInput(attrs={'class': 'form-control', 'disabled': 'disabled', 'min': '10', 'max': '200'})
        }
        labels = {

        }
        fields_required = ['title', 'description', 'detail_url', 'palette']

    def save(self, commit=True):
        instance = super(AdminFrontListForm, self).save(commit=commit)
        front_products = self.cleaned_data['front_products']
        exclude_front_products = self.cleaned_data['exclude_front_products']
        instance.products.clear()
        for f_product in front_products:
            fl_products = FrontListProduct.objects.filter(product_id=f_product.pk,
                                                          product_model=f_product.__class__.__name__)
            if fl_products.exists():
                fl_product = fl_products.first()
            else:
                fl_product = FrontListProduct(product_id=f_product.pk,
                                                          product_model=f_product.__class__.__name__)
                fl_product.save()
            instance.products.add(fl_product)

        instance.exclude_products.clear()
        for f_product in exclude_front_products:
            fl_products = FrontListProduct.objects.filter(product_id=f_product.pk,
                                                          product_model=f_product.__class__.__name__)
            if fl_products.exists():
                fl_product = fl_products.first()
            else:
                fl_product = FrontListProduct(product_id=f_product.pk,
                                              product_model=f_product.__class__.__name__)
                fl_product.save()
            instance.exclude_products.add(fl_product)

        return instance

from django import forms

from book_rental.models.sales.book import Book
from bradmin.forms.base_model_form import BRBaseModelForm
from ecommerce.models.front_list import FrontList
from ecommerce.models.sales.category import ProductCategory
from enums import FrontListRule


class AdminFrontListForm(BRBaseModelForm):

    products = forms.ModelMultipleChoiceField(label="Products",
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
    ),widget=forms.Select(attrs={'class': 'form-control'}))

    category = forms.ModelChoiceField(label="Select Category",
                                      queryset=ProductCategory.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(AdminFrontListForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FrontList
        fields = ['title', 'title_2', 'show_2', 'description',
                  'by_rule', 'rule_name', 'category', 'top_limit', 'detail_url', 'palette',
                  'products']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'palette': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {

        }
        fields_required = ['title', 'description', 'detail_url', 'palette']

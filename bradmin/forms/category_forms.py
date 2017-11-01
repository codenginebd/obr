from django import forms
from django.db.models.query_utils import Q

from bradmin.forms.base_model_form import BRBaseModelForm
from bradmin.forms.fields.category_model_choice_field import CategoryModelChoiceField
from ecommerce.models.sales.category import ProductCategory


class AdminCategoryForm(BRBaseModelForm):

    def __init__(self, *args, **kwargs):
        super(AdminCategoryForm, self).__init__(*args, **kwargs)

    parent = CategoryModelChoiceField(required=False, queryset=ProductCategory.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = ProductCategory
        fields = ['name', 'name_2', 'show_name_2', 'parent', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'name_2': forms.TextInput(attrs={'class': 'form-control'}),
            'show_name_2': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': "Name(English)",
            'name_2': "Name(Bangla)",
            'show_name_2': "Show Bangla",
            'parent': "Parent",
            'is_active': "Active",
        }
        fields_required = ['name']

    def save(self, commit=True):

        name = self.cleaned_data.get("name")
        name_2 = self.cleaned_data.get("name_2")

        filter = Q(name=name)

        if name_2:
            filter |= (Q(name=name) & Q(name_2__isnull=False) &
                                                           Q(name_2=name_2))

        category_objects = ProductCategory.objects.filter(filter)
        if not category_objects.exists():
            return super(AdminCategoryForm, self).save(commit=commit)
        error_message = ""
        if name and not name_2:
            error_message = "Category with name '%s' already exists." % name
        elif name_2:
            error_message = "Category with name '%s' or '%s' already exists." % (name, name_2)
        return ValueError(error_message)
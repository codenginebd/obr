from django import forms
from bdadmin.forms.base_form import BRBaseForm
from ecommerce.models.sales.category import ProductCategory

class AdminCategoryForm(BRBaseForm):

    def __init__(self, *args, **kwargs):
        super(AdminCategoryForm, self).__init__(*args, **kwargs)

    def make_parent_choices(self):
        all_categories = ProductCategory.objects.values_list('pk', 'name', 'name_2', flat=True)
        return tuple(tuple(a[0], a[1] + "(%s)" % a[2] if a[2] else a[1]))
        
    name = forms.CharField(label='Name(English)', required=True)
    name_bn = forms.CharField(label='Name(Bangla)', required=False)
    show_bn = forms.BooleanField(required=False)
    parent = forms.ChoiceField(choices = make_parent_choices(), label="Parent Category", initial='', widget=forms.Select(), required=False)
    
from django import forms
from bradmin.forms.base_model_form import BRBaseModelForm
from ecommerce.models.sales.warehouse import Warehouse


class AdminWarehouseForm(BRBaseModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminWarehouseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Warehouse
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-control'})
        }
        labels = {
            'name': "Name",
            'description': 'Description',
            'is_active': "Active"
        }
        fields_required = ['name', 'description']

from django import forms
from bradmin.forms.base_model_form import BRBaseModelForm
from ecommerce.models.front_palette import FrontPalette


class AdminFrontPaletteForm(BRBaseModelForm):

    order = forms.CharField(label="Palette Order",
                            widget=forms.NumberInput(attrs={"class": "form-control", "min": "1"}))

    def __init__(self, *args, **kwargs):
        super(AdminFrontPaletteForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FrontPalette
        fields = ['name', 'name_2', 'show_2', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'name_2': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {

        }
        fields_required = ['name', 'order']

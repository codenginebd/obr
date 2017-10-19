from django import forms

from bauth.models.country import Country
from bradmin.forms.base_model_form import BRBaseModelForm


class AdminCountryForm(BRBaseModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminCountryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Country
        fields = ['name', 'short_name', 'is_active']

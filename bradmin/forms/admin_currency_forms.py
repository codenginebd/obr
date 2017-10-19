from bauth.models.country import Country
from bradmin.forms.base_model_form import BRBaseModelForm
from bradmin.forms.fields.br_model_choice_field import BRBaseModelChoiceField
from payment.models.currency import Currency


class AdminCurrencyForm(BRBaseModelForm):

    country = BRBaseModelChoiceField(queryset=Country.objects.all(), label="Select Country")

    def __init__(self, *args, **kwargs):
        super(AdminCurrencyForm, self).__init__(*args, **kwargs)
        self.fields["country"].required = False
        self.fields["country"].widget.attrs["class"] = "form-control"

    class Meta:
        model = Currency
        fields = ["name", "short_name", "country", "is_active"]
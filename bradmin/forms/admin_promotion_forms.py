from django import forms
from bradmin.forms.base_model_form import BRBaseModelForm
from promotion.models.promotion import Promotion


class AdminPromotionForm(BRBaseModelForm):

    def __init__(self, *args, **kwargs):
        super(AdminPromotionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Promotion
        fields = ['title']
        widgets = {

        }
        labels = {
        }



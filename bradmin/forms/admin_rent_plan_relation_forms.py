from django import forms
from book_rental.models.sales.rent_plan_relation import RentPlanRelation
from bradmin.forms.base_model_form import BRBaseModelForm
from generics.libs.loader.loader import load_model


class AdminRentPlanRelationForm(BRBaseModelForm):

    def __init__(self, *args, **kwargs):
        super(AdminRentPlanRelationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = RentPlanRelation
        fields = []
        widgets = {

        }
        labels = {
        }



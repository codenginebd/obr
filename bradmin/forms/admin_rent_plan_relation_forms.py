from django import forms
from bradmin.forms.base_model_form import BRBaseModelForm
from ecommerce.models.rent_plan import RentPlan
from ecommerce.models.sales.rent_plan_relation import RentPlanRelation
from generics.libs.loader.loader import load_model


class AdminRentPlanForm(BRBaseModelForm):
    class Meta:
        model = RentPlan
        fields = ["name ", "days ", "is_active"]


class AdminRentPlanRelationForm(BRBaseModelForm):

    rent_plan = forms.CharField(widget=forms.TextInput(attrs={"readonly": True,
                                                              "style": "border: none; font-weight: bold;"}))

    def __init__(self, *args, **kwargs):
        super(AdminRentPlanRelationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = RentPlanRelation
        fields = ["rent_plan", "rent_rate", "is_special_offer", "special_rate", "start_time", "end_time"]
        widgets = {

        }
        labels = {
        }



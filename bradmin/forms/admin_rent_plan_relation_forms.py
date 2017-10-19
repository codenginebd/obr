from django import forms
from bradmin.forms.base_model_form import BRBaseModelForm
from bradmin.forms.fields.br_model_choice_field import BRBaseModelChoiceField
from bradmin.forms.formsets.br_base_formset import BRBaseFormSet
from ecommerce.models.rent_plan import RentPlan
from ecommerce.models.sales.rent_plan_relation import RentPlanRelation
from generics.libs.loader.loader import load_model


class AdminRentPlanForm(BRBaseModelForm):

    def __init__(self, *args, **kwargs):
        super(AdminRentPlanForm, self).__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["days"].widget.attrs["min"] = 1

    class Meta:
        model = RentPlan
        fields = ["name", "days", "is_active"]


class AdminRentPlanRelationForm(BRBaseModelForm):

    rent_plan = BRBaseModelChoiceField(queryset=RentPlan.objects.all(), label="Select Plan",
                                       widget=forms.Select(attrs={"class": "form-control",
                                                                  "style": "min-width: 140px;","disabled": "disabled"}))

    def __init__(self, *args, **kwargs):
        super(AdminRentPlanRelationForm, self).__init__(*args, **kwargs)
        initial_plan = kwargs.get("initial", None)
        if initial_plan:
            initial_plan = initial_plan.get("rent_plan", None)
        if initial_plan:
            self.fields["rent_plan"].queryset = RentPlan.objects.filter(pk=initial_plan)
        self.fields["rent_plan"].empty_label = None
        self.fields["rent_rate"].widget.attrs["class"] = "form-control"
        self.fields["rent_rate"].widget.attrs["style"] = "min-width: 120px;"

        self.fields["is_special_offer"].widget.attrs["style"] = "min-width: 120px;"

        self.fields["special_rate"].widget.attrs["class"] = "form-control"
        self.fields["special_rate"].widget.attrs["style"] = "min-width: 120px;"

        self.fields["start_time"].widget.attrs["class"] = "form-control"
        self.fields["start_time"].widget.attrs["style"] = "min-width: 120px;"

        self.fields["end_time"].widget.attrs["class"] = "form-control"
        self.fields["end_time"].widget.attrs["style"] = "min-width: 120px;"


    class Meta:
        model = RentPlanRelation
        fields = ["rent_plan", "rent_rate", "is_special_offer", "special_rate", "start_time", "end_time"]
        widgets = {
            "start_time": forms.DateInput(),
            "end_time": forms.DateInput()
        }
        labels = {
        }


class AdminRentPlanFormSet(BRBaseFormSet):
    pass



from datetime import datetime
from decimal import Decimal
from django import forms
from bradmin.forms.base_model_form import BRBaseModelForm
from bradmin.forms.fields.br_model_choice_field import BRBaseModelChoiceField
from bradmin.forms.formsets.br_base_formset import BRBaseFormSet
from ecommerce.models.rent_plan import RentPlan
from ecommerce.models.sales.rent_plan_relation import RentPlanRelation
from engine.clock.Clock import Clock
from generics.libs.loader.loader import load_model
from generics.libs.utils import get_tz_from_request


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
                                                                  "style": "min-width: 140px;"}))

    start_date = forms.CharField(label="Start Date",
                                 widget=forms.TextInput(attrs={"class": "form-control"}))

    end_date = forms.CharField(label="End Date",
                                 widget=forms.TextInput(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        if "request" in kwargs:
            self.request = kwargs.pop('request')
        else:
            self.request = None
        super(AdminRentPlanRelationForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:
            initial_plan = kwargs.get("initial", None)
            if initial_plan:
                initial_plan = initial_plan.get("rent_plan", None)
            if initial_plan:
                self.fields["rent_plan"].queryset = RentPlan.objects.filter(pk=initial_plan)
        self.fields["rent_plan"].empty_label = None
        self.fields["rent_rate"].widget.attrs["class"] = "form-control"
        self.fields["rent_rate"].widget.attrs["style"] = "min-width: 120px;"
        self.fields["rent_rate"].widget.attrs["min"] = "1.0"
        self.fields["rent_rate"].required = True

        self.fields["is_special_offer"].widget.attrs["style"] = "min-width: 120px;"

        self.fields["special_rate"].widget.attrs["class"] = "form-control"
        self.fields["special_rate"].widget.attrs["style"] = "min-width: 120px;"
        self.fields["special_rate"].required = True
        self.fields["special_rate"].widget.attrs["min"] = "1.0"

        self.fields["start_date"].widget.attrs["class"] = "form-control"
        self.fields["start_date"].widget.attrs["style"] = "min-width: 120px;"
        self.fields["start_date"].widget.attrs["readonly"] = "readonly"
        self.fields["start_date"].required = True

        self.fields["end_date"].widget.attrs["class"] = "form-control"
        self.fields["end_date"].widget.attrs["style"] = "min-width: 120px;"
        self.fields["end_date"].widget.attrs["readonly"] = "readonly"
        self.fields["end_date"].required = True


    class Meta:
        model = RentPlanRelation
        fields = ["rent_plan", "rent_rate", "is_special_offer", "special_rate", "start_date", "end_date"]

    def is_valid(self):
        prefix = self.prefix
        rent_plan = self.data.get(prefix + "-rent_plan")
        rent_rate = self.data.get(prefix + "-rent_rate")
        is_special_offer = self.data.get(prefix + "-is_special_offer")
        special_rate = self.data.get(prefix + "-special_rate")
        start_time = self.data.get(prefix + "-start_date")
        end_time = self.data.get(prefix + "-end_date")
        rent_plan = RentPlan.objects.get(pk=int(rent_plan))
        if not rent_rate:
            return False
        try:
            rent_rate = Decimal(rent_rate)
        except:
            return False
        is_special_offer = 0 if not is_special_offer else 1
        is_special_offer = bool(is_special_offer)
        if is_special_offer:
            if any([not special_rate, not start_time, not end_time]):
                return False
            try:
                special_rate = Decimal(special_rate)
            except:
                return False

            try:
                start_time = datetime.strptime(start_time, "%m/%d/%Y")
                end_time = datetime.strptime(end_time, "%m/%d/%Y")
            except:
                return False
        self.cleaned_data = {}
        self.cleaned_data["rent_plan"] = rent_plan
        self.cleaned_data["rent_rate"] = rent_rate
        self.cleaned_data["is_special_offer"] = is_special_offer
        if is_special_offer:
            self.cleaned_data["special_rate"] = special_rate
            if start_time != "0":
                self.cleaned_data["start_time"] = Clock.convert_datetime_to_utc_timestamp(start_time)
            else:
                self.cleaned_data["start_time"] = 0
            if end_time != "0":
                self.cleaned_data["end_time"] = Clock.convert_datetime_to_utc_timestamp(end_time)
            else:
                self.cleaned_data["end_time"] = 0
        return True

    def save(self, commit=True, **kwargs):
        price_matrix_instance = kwargs.get("price_matrix_instance")
        rent_plan_relation_instances = RentPlanRelation.objects.filter(price_matrix_id=price_matrix_instance.pk,
                                                        plan_id=self.cleaned_data["rent_plan"].pk)
        if rent_plan_relation_instances.exists():
            self.instance = rent_plan_relation_instances.first()
        else:
            self.instance = RentPlanRelation()

        self.instance.plan_id = self.cleaned_data["rent_plan"].pk
        self.instance.price_matrix_id = price_matrix_instance.pk
        self.instance.rent_rate = self.cleaned_data["rent_rate"]
        self.instance.is_special_offer = self.cleaned_data["is_special_offer"]
        if self.instance.is_special_offer:
            self.instance.special_rate = self.cleaned_data["special_rate"]
            self.instance.start_time = self.cleaned_data["start_time"]
            self.instance.end_time = self.cleaned_data["end_time"]
        else:
            self.instance.special_rate = Decimal(0.0)
            self.instance.start_time = 0
            self.instance.end_time = 0
        self.instance.save()
        return self.instance


class AdminRentPlanFormSet(BRBaseFormSet):

    def is_valid(self):
        return super(AdminRentPlanFormSet, self).is_valid()



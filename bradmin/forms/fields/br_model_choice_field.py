from django.forms.models import ModelChoiceField


class BRBaseModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.code
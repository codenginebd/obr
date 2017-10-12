from bradmin.forms.fields.br_model_choice_field import BRBaseModelChoiceField


class WarehouseModelChoiceField(BRBaseModelChoiceField):

    def label_from_instance(self, obj):
        return obj.name
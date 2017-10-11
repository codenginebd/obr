from bradmin.forms.fields.br_model_choice_field import BRBaseModelChoiceField


class CategoryModelChoiceField(BRBaseModelChoiceField):

    def label_from_instance(self, obj):
        if obj.name_2:
            return obj.name + "(%s)" % obj.name_2
        else:
            return obj.name
from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(BaseModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

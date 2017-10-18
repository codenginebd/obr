from django.forms.formsets import BaseFormSet


class BRBaseFormsetFactory(BaseFormSet):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, form_kwargs=None):
        super(BRBaseFormsetFactory, self).__init__(data=data, files=files, auto_id=auto_id, prefix=prefix,
                 initial=initial, form_kwargs=form_kwargs)

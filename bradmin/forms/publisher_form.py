from django import forms
from django.db.models.query_utils import Q

from book_rental.models.book_publisher import BookPublisher
from bradmin.forms.base_model_form import BRBaseModelForm


class AdminBookPublisherForm(BRBaseModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminBookPublisherForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BookPublisher
        fields = ['name', 'name_2', 'description', 'description_2','show_2', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'name_2': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'description_2': forms.Textarea(attrs={'class': 'form-control'}),
            'show_2': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': "Name(English)",
            'name_2': "Name(Bangla)",
            'description': 'Description(English)',
            'description_2': 'Description(Bangla)',
            'show_2': "Show Bangla",
            'is_active': "Active",
        }
        fields_required = ['name', 'description']

    def save(self, commit=True):
        name = self.cleaned_data.get("name")
        name_2 = self.cleaned_data.get("name_2")
        filter = Q(name=name)
        if name_2:
            filter |= (Q(name_2__isnull=False) & Q(name_2=name_2))
        publisher_objects = BookPublisher.objects.filter(filter)
        if not publisher_objects.exists():
            return super(AdminBookPublisherForm, self).save(commit=commit)
        error_message = ""
        if name and not name_2:
            error_message = "Publisher with name '%s' exist." % name
        elif name_2:
            error_message = "Publisher with name '%s' or '%s' exist" % (name, name_2)
        return ValueError(error_message)

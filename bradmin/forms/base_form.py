from django import forms


class BRBaseForm(forms.Form):
    
    def save(self, commit=True):
        instance = super(BRBaseForm, self).save(commit=commit)
        return instance
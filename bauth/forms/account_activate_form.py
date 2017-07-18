from django import forms


class AccountActivationRequestForm(forms.Form):
    email = forms.CharField(label="Email", max_length=254)

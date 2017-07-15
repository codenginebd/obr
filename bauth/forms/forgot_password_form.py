from django import forms


class PasswordResetRequestForm(forms.Form):
    email = forms.CharField(label="Email", max_length=254)

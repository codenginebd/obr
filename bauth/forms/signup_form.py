from django import forms

from bauth.validators.email_validator import validate_email
from bauth.validators.phone_number_validator import validate_phone_number


class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=200, required=True,
        widget=forms.TextInput(attrs={"class": "signup_field"})
    )
    last_name = forms.CharField(
        max_length=200, required=True,
        widget=forms.TextInput(attrs={"class": "signup_field"})
    )
    email = forms.EmailField(
        max_length=200, validators=[validate_email], required=True,
        widget=forms.TextInput(attrs={"class": "signup_field", "placeholder": "e.g someone@email.com"})
    )
    phone = forms.CharField(
        max_length=200, validators=[validate_phone_number], required=True,
        widget=forms.TextInput(attrs={"class": "signup_field", "placeholder": "1711111111"})
    )
    password = forms.CharField(
        max_length=200, required=True,
        widget=forms.PasswordInput(attrs={"class": "signup_field"})
    )
    password2 = forms.CharField(
        max_length=200, required=True,
        widget=forms.PasswordInput(attrs={"class": "signup_field"})
    )

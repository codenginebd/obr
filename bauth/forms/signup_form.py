from django import forms

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(
        attrs={"class": "signup_field"}))
    last_name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(
        attrs={"class": "signup_field"}))
    email = forms.EmailField(max_length=200, required=True, widget=forms.TextInput(
        attrs={"class": "signup_field", "placeholder": "e.g someone@email.com"}))
    phone = forms.CharField(max_length=200, required=True, widget=forms.TextInput(
        attrs={"class": "signup_field", "placeholder": "1711111111"}))
    password = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput(
        attrs={"class": "signup_field"}))
    password2 = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput(
        attrs={"class": "signup_field"}))
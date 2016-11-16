from django import forms

class SignupForm(forms.Form):
    name = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={"class": "signup_field"}))
    # last_name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(
    #     attrs={"class": "signup_field"}))
    email = forms.EmailField(max_length=200, required=True, widget=forms.TextInput(
        attrs={"class": "signup_field"}))
    phone = forms.CharField(max_length=200, required=True, widget=forms.TextInput(
        attrs={"class": "signup_field"}))
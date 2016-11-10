from django import forms

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(
        attrs={'name': 'email', "class": "form-control signup_first_name", "required": "true", 'placeholder': 'First Name'}))
    middle_name = forms.CharField(max_length=200, required=False, widget=forms.TextInput(
        attrs={'name': 'email', "class": "form-control signup_middle_name", "required": "false", 'placeholder': 'Middle Name'}))
    last_name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(
        attrs={'name': 'email', "class": "form-control signup_last_name", "required": "true", 'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=200, required=True, widget=forms.TextInput(
        attrs={'name': 'email', "class": "form-control signup_email", "required": "true",
               'placeholder': 'Enter your email'}))
    phone = forms.CharField(max_length=200, required=True, widget=forms.TextInput(
        attrs={'name': 'email', "class": "form-control signup_phone", "required": "true", 'placeholder': 'Phone Number'}))
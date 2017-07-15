from django import forms

from bauth.validators.email_validator import validate_email
from bauth.validators.phone_number_validator import validate_phone_number


class SocialSignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=200, required=True,
        widget=forms.TextInput(attrs={"readonly": True})
    )
    last_name = forms.CharField(
        max_length=200, required=True,
        widget=forms.TextInput(attrs={"readonly": True})
    )
    email = forms.EmailField(
        max_length=200, validators=[validate_email], required=True,
        widget=forms.TextInput(attrs={"class": "signup_field", "placeholder": "e.g someone@email.com"})
    )
    phone = forms.CharField(
        max_length=200, validators=[validate_phone_number], required=True,
        widget=forms.TextInput(attrs={"class": "signup_field", "placeholder": "1711111111"})
    )
    is_verified = forms.BooleanField(widget=forms.HiddenInput(), required=True, initial=False)

    def __init__(self, *args, **kwargs):
        try:
            _first_name = kwargs.pop('first_name')
            _last_name = kwargs.pop('last_name')
            _email = kwargs.pop('email')
            _phone = kwargs.pop('phone')
        except:
            _first_name = False
            _last_name = False
            _email = False
            _phone = False
        super(SocialSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['readonly'] = _first_name
        self.fields['last_name'].widget.attrs['readonly'] = _last_name
        if _email:
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['class'] = ''
            self.fields['is_verified'].initial = True
        if _phone:
            self.fields['phone'].widget.attrs['readonly'] = True
            self.fields['phone'].widget.attrs['class'] = ''

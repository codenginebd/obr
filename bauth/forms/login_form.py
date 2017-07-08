from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=200, required=True,
        widget=forms.TextInput(
            attrs={
                'name': 'email',
                "class": "form-control login_email",
                "required": "true",
                'placeholder': 'Email or Phone'
            }
        )
    )
    password = forms.CharField(
        label='', required=True,
        widget=forms.PasswordInput(
            attrs={
                'name': 'password',
                'class': 'form-control login_password',
                "required": "true",
                'placeholder': 'Password'
            }
        )
    )
    remember = forms.BooleanField(required=False)

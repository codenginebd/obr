from django.contrib.auth import authenticate, login
from django.urls.base import reverse
from django.views.generic.base import View
from bauth.forms.login_form import LoginForm
from engine.mixins.ajax_renderer_mixin import AjaxRendererMixin


class SigninAjaxView(View, AjaxRendererMixin):
    def post(self, request, *args, **kwargs):
        signin_form = LoginForm(data=request.POST)
        if signin_form.is_valid():
            username = signin_form.cleaned_data['username']
            password = signin_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                six_month = 24*60*60*30*6
                request.session.set_expiry(six_month)
                self.response['status'] = 'SUCCESS'
                self.response['message'] = 'Login Successful'
                self.response['data'] = {
                    'url': reverse('book_browse_view')
                }
                return self.render_json(self.response)

            self.response['status'] = 'FAILURE'
            self.response['message'] = 'Login Unsuccessful'
            if not username and not password:
                self.response['data'] = {
                    'message': 'Email/Phone number and Password are required'
                }
            elif username and not password:
                self.response['data'] = {
                    'message': 'Password is required'
                }
            elif not username and password:
                self.response['data'] = {
                    'message': 'Email or Phone number is required'
                }
            else:
                self.response['data'] = {
                    'message': 'Email or Password is invalid'
                }
            return self.render_json(self.response)
        else:
            self.response['status'] = 'FAILURE'
            self.response['message'] = 'Login Unsuccessful'
            self.response['data'] = { 'message': "A valid email and password is required" }
            return self.render_json(self.response)
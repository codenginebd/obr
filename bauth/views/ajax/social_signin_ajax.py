from django.contrib.auth import authenticate, login
from django.urls.base import reverse
from django.views.generic.base import View
from bauth.forms.login_form import LoginForm
from bauth.models.user import BUser
from engine.decorators.check_recaptcha import check_recaptcha
from engine.mixins.ajax_renderer_mixin import AjaxRendererMixin


class SocialSigninAjaxView(View, AjaxRendererMixin):
    def get(self, request, *args, **kwargs):
        _email = self.request.GET.get('email')
        _buser = BUser.objects.filter(user__username=_email).first()
        user = None
        if _buser and _buser.user:
            user = _buser.user
        if user is not None:
            login(request, user)
            six_month = 24 * 60 * 60 * 30 * 6
            request.session.set_expiry(six_month)
            self.response['status'] = 'SUCCESS'
            self.response['message'] = 'Login Successful'
            self.response['data'] = {
                'url': reverse('home_view')
            }
            return self.render_json(self.response)
        else:
            self.response['status'] = 'FAILURE'
            self.response['message'] = 'Login Unsuccessful'
            self.response['data'] = {
                'message': 'Email or Password is invalid'
            }
        return self.render_json(self.response)

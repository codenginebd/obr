from bauth.forms.login_form import LoginForm
from generics.views.base_template_view import BaseTemplateView
from settings import GOOGLE_RECAPTCHA_SITE_KEY, FACEBOOK_APP_ID


class LoginView(BaseTemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        context['page_title'] = 'Sign In'
        context['captcha_site_key'] = GOOGLE_RECAPTCHA_SITE_KEY
        context['facebook_app_id'] = FACEBOOK_APP_ID
        return context

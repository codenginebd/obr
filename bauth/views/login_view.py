from bauth.forms.login_form import LoginForm
from generics.views.base_template_view import BaseTemplateView


class LoginView(BaseTemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        context['page_title'] = 'Sign In'
        return context
from django.views.generic.base import TemplateView

from bauth.forms.signup_form import SignupForm


class SignupView(TemplateView):
    template_name = "signup.html"

    def get_context_data(self, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)
        context['signup_form'] = SignupForm()
        return context
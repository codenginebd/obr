from bauth.forms.signup_form import SignupForm
from generics.views.base_template_view import BaseTemplateView


class SignupView(BaseTemplateView):
    template_name = "signup.html"

    def get_context_data(self, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)
        context["page_title"] = "Sign Up"
        context['signup_form'] = SignupForm()
        return context
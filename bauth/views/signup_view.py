from bauth.forms.signup_form import SignupForm
from generics.views.base_template_view import BaseTemplateView
from settings import FACEBOOK_APP_ID


class SignupView(BaseTemplateView):
    template_name = "signup.html"

    def get_context_data(self, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)
        context["page_title"] = "Sign Up"
        context['signup_form'] = SignupForm()
        context['facebook_app_id'] = FACEBOOK_APP_ID
        return context
    
    def post(self, **kwargs):
        form_instance = SignupForm(self.request.POST)
        if form_instance.is_valid():
            form_instance.save()
            #Send email here
        else:
            pass
from bauth.forms.signup_form import SignupForm
from bauth.forms.social_signup_form import SocialSignupForm
from generics.views.base_template_view import BaseTemplateView


class SocialSignupView(BaseTemplateView):
    template_name = "social_signup.html"

    def get_context_data(self, **kwargs):
        context = super(SocialSignupView, self).get_context_data(**kwargs)
        context["page_title"] = "Social Sign Up"
        _initial = {
            'first_name': self.request.GET.get('first_name', ''),
            'last_name': self.request.GET.get('last_name', ''),
            'email': self.request.GET.get('email', ''),
            'phone': self.request.GET.get('phone', '')
        }
        _readonly_field = {
            'first_name': True,
            'last_name': True,
            'email': True if self.request.GET.get('email') else False,
            'phone': True if self.request.GET.get('phone') else False
        }
        context['signup_form'] = SocialSignupForm(initial=_initial, **_readonly_field)
        return context
    
    def post(self, **kwargs):
        form_instance = SocialSignupForm(self.request.POST)
        if form_instance.is_valid():
            form_instance.save()
            #Send email here
        else:
            pass
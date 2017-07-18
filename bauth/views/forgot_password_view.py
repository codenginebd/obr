from bauth.forms.forgot_password_form import PasswordResetRequestForm
from generics.views.base_template_view import BaseTemplateView


class ResetPasswordRequestView(BaseTemplateView):
    template_name = "forgot_password.html"

    def get_context_data(self, **kwargs):
        context = super(ResetPasswordRequestView, self).get_context_data(**kwargs)
        context['forgot_password_form'] = PasswordResetRequestForm()
        return context

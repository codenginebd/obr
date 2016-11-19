from django.views.generic.base import View

from bauth.forms.signup_form import SignupForm
from engine.mixins.ajax_renderer_mixin import AjaxRendererMixin


class SignupAjaxView(View, AjaxRendererMixin):
    def post(self, request, *args, **kwargs):
        signup_form_instance = SignupForm(request.POST)
        if signup_form_instance.is_valid():
            pass
        ajax_response = self.render_json(self.response)
        return ajax_response
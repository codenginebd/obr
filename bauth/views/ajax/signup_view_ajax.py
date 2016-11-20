from django.contrib.auth.models import User
from django.views.generic.base import View
from django.db import transaction
from bauth.forms.signup_form import SignupForm
from bauth.models.user import BUser
from engine.mixins.ajax_renderer_mixin import AjaxRendererMixin


class SignupAjaxView(View, AjaxRendererMixin):
    def post(self, request, *args, **kwargs):
        signup_form_instance = SignupForm(request.POST)
        if signup_form_instance.is_valid():
            with transaction.atomic():

                auth_user_fields = {
                    'first_name': signup_form_instance.cleaned_data['first_name'],
                    'last_name': signup_form_instance.cleaned_data['last_name'],
                    'username': signup_form_instance.cleaned_data['email'],
                    'email': signup_form_instance.cleaned_data['email'],
                    'password': signup_form_instance.cleaned_data['password'],
                    'is_active': False
                }

                auth_user = User.objects.create_user(**auth_user_fields)

                br_user_instance = BUser()
                br_user_instance.user_id = auth_user.pk
                br_user_instance.phone = signup_form_instance.cleaned_data['phone']
                br_user_instance.social_signup = False
                br_user_instance.save()

        self.response['status'] = 'SUCCESS'
        self.response['message'] = 'Successful'
        self.response['data'] = {
            'email': br_user_instance.user.email
        }
        ajax_response = self.render_json(self.response)
        return ajax_response
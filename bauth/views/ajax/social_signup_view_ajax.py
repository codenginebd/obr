from django.contrib.auth.models import User
from django.views.generic.base import View
from django.db import transaction
from bauth.forms.social_signup_form import SocialSignupForm
from bauth.models.user import BUser
from engine.mixins.ajax_renderer_mixin import AjaxRendererMixin
from django.urls.base import reverse
from django.contrib.auth import login


class SocialSignupAjaxView(View, AjaxRendererMixin):
    def post(self, request, *args, **kwargs):
        signup_form_instance = SocialSignupForm(request.POST)
        if signup_form_instance.is_valid():
            self.response['data'] = dict()
            with transaction.atomic():
                auth_user_fields = {
                    'first_name': signup_form_instance.cleaned_data['first_name'],
                    'last_name': signup_form_instance.cleaned_data['last_name'],
                    'username': signup_form_instance.cleaned_data['email'],
                    'email': signup_form_instance.cleaned_data['email'],
                    'is_active': True
                }

                auth_user = User.objects.create_user(**auth_user_fields)

                br_user_instance = BUser()
                br_user_instance.user_id = auth_user.pk
                br_user_instance.phone = signup_form_instance.cleaned_data['phone']
                br_user_instance.is_verified = signup_form_instance.cleaned_data['is_verified']
                br_user_instance.social_signup = True
                br_user_instance.save()

                if br_user_instance.is_verified:
                    login(request, auth_user)
                    six_month = 24 * 60 * 60 * 30 * 6
                    request.session.set_expiry(six_month)
                    self.response['data'].update({
                        'success_url': reverse('home_view')
                    })

            self.response['status'] = 'SUCCESS'
            self.response['message'] = 'Successful'
            self.response['data'].update({
                'email': br_user_instance.user.email,
            })
        ajax_response = self.render_json(self.response)
        return ajax_response

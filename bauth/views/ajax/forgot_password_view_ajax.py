from bauth.forms.forgot_password_form import PasswordResetRequestForm
from bauth.models.user import BUser
from config.settings.email_config import DEFAULT_FROM_EMAIL
from engine.mixins.ajax_renderer_mixin import AjaxRendererMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import *

from settings import SITE_NAME


class ResetPasswordRequestAjaxView(View, AjaxRendererMixin):
    @staticmethod
    def validate_email_address(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email"]
        if self.validate_email_address(data) is True:
            b_users = BUser.objects.filter(user__username=str(data), user__is_active=True)
            if b_users.exists():
                for b_user in b_users:
                    if b_user.user:
                        c = {
                            'email': b_user.user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': SITE_NAME,
                            'uid': urlsafe_base64_encode(force_bytes(b_user.user.pk)),
                            'user': b_user.user,
                            'token': default_token_generator.make_token(b_user.user),
                            'protocol': 'http',
                        }
                        subject_template_name = 'registration/password_reset_subject.txt'
                        email_template_name = 'password_reset_email.html'
                        subject = loader.render_to_string(subject_template_name, c)
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)

                        # sending email
                        # send_mail(subject, email, DEFAULT_FROM_EMAIL, [b_user.user.email], fail_silently=False)

                        self.response['status'] = 'SUCCESS'
                        self.response['message'] = 'Forgot Password Request successful'
                        self.response['data'] = {
                            'email': b_user.user.email
                        }
                        return self.render_json(self.response)

                self.response['status'] = 'FAILURE'
                self.response['message'] = 'Forgot Password Request unsuccessful'
                self.response['data'] = {
                    'message': "User associated with this username does not have authentication privileges."
                }
                return self.render_json(self.response)

            self.response['status'] = 'FAILURE'
            self.response['message'] = 'Forgot Password Request unsuccessful'
            self.response['data'] = {
                'message': "This email does not exist in the system."
            }
            return self.render_json(self.response)

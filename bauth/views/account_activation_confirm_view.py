from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.views.generic.edit import FormView
from engine.mixins.ajax_renderer_mixin import AjaxRendererMixin
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth import login


class AccountActivationConfirmView(FormView, AjaxRendererMixin):
    def get(self, request, uidb64=None, token=None, *arg, **kwargs):
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and user.buser is not None and default_token_generator.check_token(user, token):
            b_user = user.buser
            b_user.is_verified = True
            b_user.save()
            login(request, user)
            six_month = 24 * 60 * 60 * 30 * 6
            request.session.set_expiry(six_month)
            return HttpResponseRedirect(reverse('home_view'))
        else:
            return HttpResponseRedirect(reverse('bauth_login_view'))

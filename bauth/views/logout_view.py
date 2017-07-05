from django.contrib.auth.views import logout
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from generics.views.base_view import BaseView


class LogoutView(BaseView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('bauth_login_view'))
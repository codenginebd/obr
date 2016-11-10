from django.conf.urls import url

from bauth.views.login_view import LoginView
from bauth.views.signup_view import SignupView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="bauth_login_view"),
    url(r'^signup/$', SignupView.as_view(), name="bauth_signup_view"),
]

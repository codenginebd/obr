from django.conf.urls import url

from bauth.views.ajax.signup_view_ajax import SignupAjaxView
from bauth.views.login_view import LoginView
from bauth.views.signup_view import SignupView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="bauth_login_view"),
    url(r'^signup/$', SignupView.as_view(), name="bauth_signup_view"),
]

# All ajax urls
urlpatterns += [
    url(r'^ajax/signup/$', SignupAjaxView.as_view(), name="bauth_ajax_signup_view"),
]

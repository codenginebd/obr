from django.conf.urls import url

from bauth.views.ajax.check_email_views import CheckEmailView
from bauth.views.ajax.check_phone_view import CheckPhoneView
from bauth.views.ajax.signup_view_ajax import SignupAjaxView
from bauth.views.login_view import LoginView
from bauth.views.post_signup_view import PostSignupView
from bauth.views.signup_view import SignupView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="bauth_login_view"),
    url(r'^signup/$', SignupView.as_view(), name="bauth_signup_view"),
    url(r'^signup-complete/$', PostSignupView.as_view(), name="bauth_post_signup_view"),
]

# All ajax urls
urlpatterns += [
    url(r'^ajax/signup/$', SignupAjaxView.as_view(), name="bauth_ajax_signup_view"),
    url(r'^ajax/check-email/$', CheckEmailView.as_view(), name="bauth_ajax_check_email_view"),
    url(r'^ajax/check-phone/$', CheckPhoneView.as_view(), name="bauth_ajax_check_phone_view"),
]

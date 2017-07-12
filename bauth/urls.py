from django.conf.urls import url
from bauth.views.ajax.check_email_views import CheckEmailView
from bauth.views.ajax.check_phone_view import CheckPhoneView
from bauth.views.ajax.forgot_password_view_ajax import ResetPasswordRequestAjaxView
from bauth.views.ajax.signin_ajax import SigninAjaxView
from bauth.views.ajax.signup_view_ajax import SignupAjaxView
from bauth.views.forgot_password_view import ResetPasswordRequestView
from bauth.views.login_view import LoginView
from bauth.views.logout_view import LogoutView
from bauth.views.password_reset_confirm_view import PasswordResetConfirmView
from bauth.views.post_forgot_password_view import PostForgotPasswordView
from bauth.views.post_signup_view import PostSignupView
from bauth.views.signup_view import SignupView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="bauth_login_view"),
    url(r'^logout/$', LogoutView.as_view(), name="bauth_logout_view"),
    url(r'^signup/$', SignupView.as_view(), name="bauth_signup_view"),
    url(r'^signup-complete/$', PostSignupView.as_view(), name="bauth_post_signup_view"),
    url(r'^forgot_password/$', ResetPasswordRequestView.as_view(), name="bauth_forgot_password"),
    url(r'^forgot_password-complete/$', PostForgotPasswordView.as_view(), name="bauth_post_forgot_password_view"),
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(),
        name='bauth_reset_password_confirm'),
]

# All ajax urls
urlpatterns += [
    url(r'^ajax/login/$', SigninAjaxView.as_view(), name="bauth_ajax_login_view"),
    url(r'^ajax/signup/$', SignupAjaxView.as_view(), name="bauth_ajax_signup_view"),
    url(r'^ajax/check-email/$', CheckEmailView.as_view(), name="bauth_ajax_check_email_view"),
    url(r'^ajax/check-phone/$', CheckPhoneView.as_view(), name="bauth_ajax_check_phone_view"),
    url(r'^ajax/forgot_password/$', ResetPasswordRequestAjaxView.as_view(), name="bauth_ajax_forgot_password"),
]

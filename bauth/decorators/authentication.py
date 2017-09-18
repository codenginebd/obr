from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import HttpResponseRedirect
from django.utils.decorators import method_decorator


def br_login_required(login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url
    )
    return actual_decorator


class UserLoginRequired(object):
    @method_decorator(br_login_required(login_url=settings.USER_LOGIN_URL))
    def dispatch(self,request, *args, **kwargs):
        dispatched = super(UserLoginRequired, self).dispatch(request,*args,**kwargs)
        if request.user.is_staff or request.user.is_superuser:
            return HttpResponseRedirect(settings.USER_LOGIN_URL)
        return dispatched


class AdminLoginRequired(object):
    @method_decorator(br_login_required(login_url=settings.ADMIN_LOGIN_URL))
    def dispatch(self,request, *args, **kwargs):
        dispatched = super(AdminLoginRequired, self).dispatch(request,*args,**kwargs)
        if not request.user.is_staff:
            return HttpResponseRedirect(settings.ADMIN_LOGIN_URL)
        return dispatched
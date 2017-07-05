from django.contrib.auth.models import User
from django.views.generic.base import View

from bauth.models.user import BUser
from engine.mixins.ajax_renderer_mixin import AjaxRendererMixin


class CheckPhoneView(View, AjaxRendererMixin):
    def get(self, request, *args, **kwargs):
        value = request.GET.get('value')
        if BUser.objects.filter(phone=value).exists():
            self.response['status'] = 'SUCCESS'
            self.response['message'] = 'Already Exists'
            self.response['code'] = 1
            return self.render_json(self.response)
        self.response['status'] = 'FAILURE'
        self.response['message'] = 'Available'
        self.response['code'] = 0
        return self.render_json(self.response)
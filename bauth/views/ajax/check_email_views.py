from django.contrib.auth.models import User
from django.views.generic.base import View

from engine.mixins.ajax_renderer_mixin import AjaxRendererMixin


class CheckEmailView(View, AjaxRendererMixin):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('value')
        if User.objects.filter(username=email).exists():
            self.response['status'] = 'SUCCESS'
            self.response['message'] = 'Already Exists'
            self.response['code'] = 1
            return self.render_json(self.response)
        self.response['status'] = 'FAILURE'
        self.response['message'] = 'Available'
        self.response['code'] = 0
        return self.render_json(self.response)

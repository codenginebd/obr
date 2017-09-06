from django.views.generic.base import View


class BaseView(View):

    def get_context_data(self, request, *args, **kwargs):
        return {}
        
    def prepare_response(self, request, context, *args, **kwargs):
        return {}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, *args, **kwargs)
        response = self.prepare_response(request, context, *args, **kwargs)
        return response
        
    def post(self, request, *args, **kwargs):
        pass
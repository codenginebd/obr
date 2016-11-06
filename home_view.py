from django.http.response import HttpResponse

from generics.loader.template_loader import TemplateLoader
from generics.views.base_view import BaseView


class HomeView(BaseView):
    template_name = "public/home.html"

    def get(self, request, *args, **kwargs):
        return HttpResponse(TemplateLoader.load_template(self.template_name, {}))
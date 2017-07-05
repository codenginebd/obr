from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse

from generics.loader.template_loader import TemplateLoader
from generics.views.base_view import BaseView


class HomeView(BaseView):
    template_name = "public/home.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('book_browse_view'))
        return HttpResponse(TemplateLoader.load_template(self.template_name, {}))
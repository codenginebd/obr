from django.views.generic.base import TemplateView


class BaseTemplateView(TemplateView):

    def get_page_title(self):
        return ""

    def get_context_data(self, **kwargs):
        context = super(BaseTemplateView, self).get_context_data(**kwargs)
        context["page_title"] = self.get_page_title()
        return context


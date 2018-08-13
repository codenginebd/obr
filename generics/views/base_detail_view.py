from django.views.generic import DetailView


class BaseDetailView(DetailView):
    def get_page_title(self):
        return ""

    def get_context_data(self, **kwargs):
        context = super(BaseDetailView, self).get_context_data(**kwargs)
        context["page_title"] = self.get_page_title()
        return context

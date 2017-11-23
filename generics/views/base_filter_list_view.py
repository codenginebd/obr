from generics.views.base_list_view import BaseListView


class BaseFilterListView(BaseListView):
    paginate_by = 20
    template_name = "base_filter_list_view.html"
    
    def get_filter_context(self):
        return {}

    def get_filter_templates(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(BaseListView, self).get_context_data(**kwargs)
        context["filter_template"] = self.get_filter_template()
        return context
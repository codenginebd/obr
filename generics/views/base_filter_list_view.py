from generics.views.base_list_view import BaseListView
from generics.loader.template_loader import TemplateLoader


class BaseFilterListView(BaseListView):
    paginate_by = 20
    template_name = "base_filter_list_view.html"
    
    def get_filter_context(self, request, **kwargs):
        return {}

    def get_filter_template(self):
        return None
        
    def render_filter_template(self, request, **kwargs):
        template = self.get_filter_template()
        context = self.get_filter_context(request=request, **kwargs)
        if template and context:
            rendered_template = TemplateLoader.load_template(template_name=template, context=context)
            return rendered_template
        return None

    def get_context_data(self, **kwargs):
        context = super(BaseListView, self).get_context_data(**kwargs)
        context["filter_template"] = self.render_filter_template(request=self.request, **kwargs)
        return context
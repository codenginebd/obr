from django.views.generic.base import TemplateView
from bradmin.mixins.AdminTemplateMixin import AdminTemplateMixin


class AdminBaseTemplateView(AdminTemplateMixin, TemplateView):

    def get_left_menu_items(self):
        return {}

    def get_content_data(self):
        return {}

    def get_context_data(self, **kwargs):
        context = super(AdminBaseTemplateView, self).get_context_data(**kwargs)
        context["left_menu_items"] = self.get_left_menu_items()
        context["content"] = self.get_content_data()
        return context
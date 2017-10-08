from django.views.generic.detail import DetailView
from bradmin.mixins.admin_action_button_mixin import AdminActionButtonMixin
from bradmin.mixins.admin_list_menu_mixin import AdminListMenuMixin


class BaseDetailView(AdminActionButtonMixin, AdminListMenuMixin, DetailView):

    def get_template_names(self):
        return []

    def get_object(self, queryset=None):
        return super(BaseDetailView, self).get_object(queryset=queryset)

    def get_queryset(self):
        return super(BaseDetailView, self).get_queryset()

    def get_context_object_name(self, obj):
        return super(BaseDetailView, self).get_context_object_name(obj=obj)

    def get_page_title(self):
        return "BDReads.com"

    def get_ttab_name(self):
        return ""

    def get_ltab_name(self):
        return ""

    def get_context_data(self, **kwargs):
        context = super(BaseDetailView, self).get_context_data(kwargs=kwargs)
        context["details_action"] = True
        context["page_title"] = self.get_page_title()
        context["show_edit"] = self.show_edit()
        context["show_delete"] = self.show_delete()
        context["show_activate"] = self.show_activate()
        context["show_deactivate"] = self.show_deactivate()
        context["edit_link"] = self.get_edit_link(object_id=self.object.pk)
        context["delete_link"] = self.get_delete_link()
        context["list_url"] = self.model.get_list_url()
        context["activate_link"] = self.get_activate_link()
        context["deactivate_link"] = self.get_deactivate_link()
        context["breadcumb"] = self.get_breadcumb(request=self.request)
        context["left_menu_items"] = self.get_left_menu_items()
        context["ttab"] = self.get_ttab_name()
        context["ltab"] = self.get_ltab_name()
        return context
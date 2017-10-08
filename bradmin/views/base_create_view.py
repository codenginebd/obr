from django.views.generic.edit import CreateView
from django.contrib import messages

from bradmin.mixins.admin_list_menu_mixin import AdminListMenuMixin


class BRBaseCreateView(AdminListMenuMixin, CreateView):

    def get_form_title(self):
        return "Create"

    def get_submit_url(self):
        return ""

    def get_cancel_url(self):
        return ""

    def get_page_title(self):
        return "BDReads.com"

    def get_success_url(self):
        return super(BRBaseCreateView, self).get_success_url()

    def get_context_data(self, **kwargs):
        context = super(BRBaseCreateView, self).get_context_data(**kwargs)
        context["page_title"] = self.get_page_title()
        context["form_title"] = self.get_form_title()
        context["submit_url"] = self.get_submit_url()
        context["cancel_url"] = self.get_cancel_url()
        context["breadcumb"] = self.get_breadcumb(request=self.request)
        context["left_menu_items"] = self.get_left_menu_items()
        return context

    def get(self, request, *args, **kwargs):
        return super(BRBaseCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(BRBaseCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        messages.add_message(request=self.request, level=messages.INFO,
                             message="Created Successfully")
        return super(BRBaseCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(BRBaseCreateView, self).form_invalid(form=form)
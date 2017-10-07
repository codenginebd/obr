from django.views.generic.edit import UpdateView
from django.contrib import messages


class BRBaseUpdateView(UpdateView):
    def get_form_title(self):
        return "Update"

    def get_submit_url(self):
        return ""

    def get_cancel_url(self):
        return ""

    def get_success_url(self):
        return ""

    def get_page_title(self):
        return "BDReads.com"

    def get_context_data(self, **kwargs):
        context = super(BRBaseUpdateView, self).get_context_data(**kwargs)
        context["page_title"] = self.get_page_title()
        context["form_title"] = self.get_form_title()
        context["submit_url"] = self.get_submit_url()
        context["cancel_url"] = self.get_cancel_url()
        return context

    def get(self, request, *args, **kwargs):
        return super(BRBaseUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(BRBaseUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        messages.add_message(request=self.request, level=messages.INFO,
                             message="Updated Successfully")
        return super(BRBaseUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(BRBaseUpdateView, self).form_invalid(form=form)
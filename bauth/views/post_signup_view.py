from generics.views.base_template_view import BaseTemplateView


class PostSignupView(BaseTemplateView):
    template_name = "post_signup_view.html"

    def get_context_data(self, **kwargs):
        context = super(PostSignupView, self).get_context_data(**kwargs)
        context["page_title"] = "Sign Up Completed"
        context['email'] = self.request.GET.get('email')
        return context
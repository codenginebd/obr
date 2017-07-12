from generics.views.base_template_view import BaseTemplateView


class PostForgotPasswordView(BaseTemplateView):
    template_name = "post_forgot_password_view.html"

    def get_context_data(self, **kwargs):
        context = super(PostForgotPasswordView, self).get_context_data(**kwargs)
        context["page_title"] = "Forgot Password Request Successfully Send"
        context['email'] = self.request.GET.get('email')
        return context

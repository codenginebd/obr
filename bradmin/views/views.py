from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.base import TemplateView, View
from django.contrib import messages

from bauth.decorators.authentication import AdminLoginRequired


class AdminLoginView(TemplateView):
    template_name = "admin/login.html"
    page_title = "Admin Login"

    def get_context_data(self, **kwargs):
        context = super(AdminLoginView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        return context

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not email or not password:
            messages.add_message(request, messages.INFO, 'Email and password required')
            return HttpResponseRedirect(reverse("admin_login_view"))
        else:
            user = authenticate(username=email, password=password)
            if user and user.is_staff is True:
                login(request, user)
                return HttpResponseRedirect(reverse("admin_home_view"))

            else:
                messages.add_message(request, messages.INFO, 'Invalid Email or Password')
                return HttpResponseRedirect(reverse("admin_login_view"))


class AdminHomeView(AdminLoginRequired, TemplateView):
    template_name = "admin/home.html"
    page_title = "Admin Home"

    def get_context_data(self, **kwargs):
        context = super(AdminHomeView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        return context

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse("admin_category_view"))
        # return render(request, self.template_name,context={})

class AdminLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.INFO, 'You are logged out')
        return HttpResponseRedirect(reverse("admin_login_view"))
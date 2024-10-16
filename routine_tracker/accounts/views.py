from typing import Any

from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView

from routine_tracker.accounts.forms import RegistrationForm
from routine_tracker.accounts.models import UserProfile

User = get_user_model()


class LoginView(LoginView):
    template_name = "accounts/form.html"
    extra_context = {
        "title": "Login",
        "submit": "Login",
        "layout": "layouts/empty.html",
    }


class RegistrationView(FormView):
    template_name = "accounts/form.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("base:index")
    extra_context = {
        "title": "Register",
        "submit": "Register",
        "layout": "layouts/empty.html",
    }

    def form_valid(self, form: RegistrationForm) -> HttpResponse:
        # Save the user
        user = form.save()

        # Log the user in for current session
        login(self.request, user)

        # Redirect to success url
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    context_object_name = "profile"
    template_name = "accounts/profile.html"

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> UserProfile:
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)

        return profile


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/form.html"
    success_url = reverse_lazy("accounts:profile")
    is_success = False
    extra_context = {
        "title": "Change Password",
        "submit": "Change Password",
        "layout": "layouts/default.html",
        "boost": True,
    }

    def form_valid(self, form: Any) -> HttpResponse:
        # Save the form
        response = super().form_valid(form)
        # Set the success flag
        self.is_success = True
        # Return the response
        return response

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        response = super().get(request, *args, **kwargs)

        if self.is_success:
            response.headers["HX-Redirect"] = self.success_url

        return response


class LogoutView(LoginRequiredMixin, LogoutView):
    pass

from typing import Any

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from routine_tracker.accounts.forms import RegistrationForm, UserForm, UserProfileForm
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


class UserProfileFormView(LoginRequiredMixin, FormView):
    template_name = "accounts/profile.html"

    def get_form_instance(self) -> Any:
        return None

    def get_form_kwargs(self) -> dict[str, Any]:
        # Get the form kwargs
        kwargs = super().get_form_kwargs()

        # Add the instance to the kwargs if it exists
        if (instance := self.get_form_instance()) is not None:
            kwargs["instance"] = instance

        return kwargs

    def get_success_url(self) -> str:
        return self.request.path

    def form_valid(self, form: UserProfileForm) -> HttpResponse:
        form.save()
        messages.success(self.request, _("Profile updated successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Profile update failed"))
        return super().form_invalid(form)


class UserEditView(UserProfileFormView):
    model = User
    form_class = UserForm

    def get_form_instance(self) -> Any:
        return self.request.user


class UserSettingsView(UserProfileFormView):
    model = UserProfile
    form_class = UserProfileForm

    def get_form_instance(self) -> Any:
        return self.request.user.profile

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        response = super().get(request, *args, **kwargs)

        if not request.headers.get("HX-Navigation") == "true":
            response.headers["HX-Refresh"] = "true"

        return response


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

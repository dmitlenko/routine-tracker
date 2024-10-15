from typing import Any

from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models.query import QuerySet
from django.http import HttpResponse
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


class ProfileView(DetailView):
    model = UserProfile
    context_object_name = "profile"
    template_name = "accounts/profile.html"

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> UserProfile:
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)

        return profile


class LogoutView(LogoutView):
    pass

from django.urls import path

from .views import ChangePasswordView, LoginView, LogoutView, RegistrationView, UserEditView, UserSettingsView

app_name = "accounts"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("profile/", UserEditView.as_view(), name="profile"),
    path("settings/", UserSettingsView.as_view(), name="settings"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("changepassword/", ChangePasswordView.as_view(), name="change-password"),
]

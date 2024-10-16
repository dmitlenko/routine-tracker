from django.urls import path

from .views import ChangePasswordView, LoginView, LogoutView, ProfileView, RegistrationView

app_name = "accounts"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("changepassword/", ChangePasswordView.as_view(), name="change-password"),
]

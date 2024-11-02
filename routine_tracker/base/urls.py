from django.urls import path

from .views import DashboardView

app_name = "base"

urlpatterns = [
    path("", DashboardView.as_view(), name="index"),
]

from django.urls import path

from .views import RoutineGroupDetailView, RoutineGroupListView

app_name = "routines"

urlpatterns = [
    path("groups/", RoutineGroupListView.as_view(), name="routine-group-list"),
    path("groups/<int:pk>/", RoutineGroupDetailView.as_view(), name="routine-group-detail"),
]

from django.urls import path

from .views import RoutineCreateView, RoutineGroupCreateView, RoutineGroupDetailView, RoutineGroupListView

app_name = "routines"

urlpatterns = [
    path("groups/", RoutineGroupListView.as_view(), name="routine-group-list"),
    path("groups/create/", RoutineGroupCreateView.as_view(), name="routine-group-create"),
    path("groups/<int:pk>/", RoutineGroupDetailView.as_view(), name="routine-group-detail"),
    path("groups/<int:pk>/routine/create", RoutineCreateView.as_view(), name="routine-create"),
]

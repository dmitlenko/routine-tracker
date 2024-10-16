from django.urls import path

from .views import (
    EntryCreateView,
    RoutineCreateView,
    RoutineGroupCreateView,
    RoutineGroupDetailView,
    RoutineGroupListView,
)

app_name = "routines"

urlpatterns = [
    path("groups/", RoutineGroupListView.as_view(), name="routine-group-list"),
    path("groups/create/", RoutineGroupCreateView.as_view(), name="routine-group-create"),
    path("groups/<int:pk>/", RoutineGroupDetailView.as_view(), name="routine-group-detail"),
    path("groups/<int:pk>/routine/create", RoutineCreateView.as_view(), name="routine-create"),
    path("groups/<int:pk>/routine/<int:routine_id>/create_entry", EntryCreateView.as_view(), name="entry-create"),
]

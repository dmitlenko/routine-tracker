from django.urls import path

from .views import (
    EntryCreateView,
    RoutineCreateView,
    RoutineGroupCreateView,
    RoutineGroupDeleteView,
    RoutineGroupDetailView,
    RoutineGroupListView,
    RoutineGroupUpdateView,
)

app_name = "routines"

urlpatterns = [
    path("groups/", RoutineGroupListView.as_view(), name="group-list"),
    path("groups/<int:pk>/", RoutineGroupDetailView.as_view(), name="group-detail"),
    path("groups/<int:pk>/routine/create", RoutineCreateView.as_view(), name="routine-create"),
    path("groups/<int:pk>/routine/<int:routine_id>/create_entry", EntryCreateView.as_view(), name="entry-create"),
]

htmx_patterns = [
    path("groups/create/", RoutineGroupCreateView.as_view(), name="group-create"),
    path("groups/<int:pk>/delete", RoutineGroupDeleteView.as_view(), name="group-delete"),
    path("groups/<int:pk>/edit-modal", RoutineGroupUpdateView.as_view(), name="group-edit-modal"),
]

urlpatterns += htmx_patterns

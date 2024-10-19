from django.urls import path

from .views import (
    EntryCreateView,
    RoutineCreateView,
    RoutineDeleteView,
    RoutineDetailView,
    RoutineGroupCreateView,
    RoutineGroupDeleteView,
    RoutineGroupDetailView,
    RoutineGroupListView,
    RoutineGroupUpdateView,
    RoutineUpdateView,
)

app_name = "routines"

urlpatterns = [
    path("groups/", RoutineGroupListView.as_view(), name="group-list"),
    path("groups/<int:pk>/", RoutineGroupDetailView.as_view(), name="group-detail"),
    path("groups/<int:pk>/routine/<int:routine_id>/create_entry", EntryCreateView.as_view(), name="entry-create"),
]

htmx_patterns = [
    path("groups/create/", RoutineGroupCreateView.as_view(), name="group-create"),
    path("groups/<int:pk>/delete", RoutineGroupDeleteView.as_view(), name="group-delete"),
    path("groups/<int:pk>/edit-modal", RoutineGroupUpdateView.as_view(), name="group-edit-modal"),
    path("groups/<int:pk>/routine/create", RoutineCreateView.as_view(), name="routine-create"),
    path("groups/<int:group_id>/routine/<int:pk>/", RoutineDetailView.as_view(), name="routine-detail"),
    path("groups/<int:group_id>/routine/<int:pk>/edit", RoutineUpdateView.as_view(), name="routine-edit-modal"),
    path("groups/<int:group_id>/routine/<int:pk>/delete", RoutineDeleteView.as_view(), name="routine-delete"),
]

urlpatterns += htmx_patterns

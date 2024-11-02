from django.urls import path

from routine_tracker.routines.views.entry import EntryDeleteView, EntryUpdateView

from .views import (
    EntryCreateView,
    EntryExportView,
    EntryTableView,
    RoutineChartView,
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
]

htmx_patterns = [
    # Groups
    path("groups/create/", RoutineGroupCreateView.as_view(), name="group-create"),
    path("groups/<int:pk>/delete", RoutineGroupDeleteView.as_view(), name="group-delete"),
    path("groups/<int:pk>/edit-modal", RoutineGroupUpdateView.as_view(), name="group-edit-modal"),
    # Routines
    path("groups/<int:pk>/routine/create", RoutineCreateView.as_view(), name="routine-create"),
    path("routine/<int:pk>/", RoutineDetailView.as_view(), name="routine-detail"),
    path("routine/<int:pk>/edit", RoutineUpdateView.as_view(), name="routine-edit-modal"),
    path("routine/<int:pk>/delete", RoutineDeleteView.as_view(), name="routine-delete"),
    path("routine/<int:pk>/entires", EntryTableView.as_view(), name="entry-table"),
    path("routine/<int:pk>/export", EntryExportView.as_view(), name="entry-export"),
    # Entries
    path("routine/<int:pk>/entry/create", EntryCreateView.as_view(), name="entry-create"),
    path("entry/<int:pk>/edit", EntryUpdateView.as_view(), name="entry-edit-modal"),
    path("entry/<int:pk>/delete", EntryDeleteView.as_view(), name="entry-delete"),
    # Charts
    path("routine/<int:pk>/statistics", RoutineChartView.as_view(), name="routine-chart"),
]

urlpatterns += htmx_patterns

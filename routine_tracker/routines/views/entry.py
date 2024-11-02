import csv
import json
from typing import Any, List

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from routine_tracker.base.utils.htmx import custom_swap
from routine_tracker.base.utils.modal import close_modal
from routine_tracker.core.mixins import ModalDeleteMixin, ModalFormMixin
from routine_tracker.routines.components.entry_table.entry_table import EntryTableComponent
from routine_tracker.routines.utils.chart import update_chart
from routine_tracker.routines.utils.export import file_response

from ..forms import RoutineEntryForm, RoutineForm
from ..models import Routine, RoutineEntry


class EntryCreateView(LoginRequiredMixin, ModalFormMixin, CreateView):
    model = RoutineEntry
    form_class = RoutineEntryForm
    template_name = "routines/entries/form.html"
    title = _("Create Entry")
    button_text = _("Create")

    def get_routine(self) -> Routine:
        return get_object_or_404(Routine, pk=self.kwargs["pk"], group__user=self.request.user)

    def get_form_url(self) -> str:
        return reverse("routines:entry-create", kwargs={"pk": self.kwargs["pk"]})

    def get_success_url(self) -> str:
        return reverse("routines:group-detail", kwargs={"pk": self.get_routine().group.pk})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["routine"] = get_object_or_404(Routine, pk=self.kwargs["pk"], group__user=self.request.user)
        return context

    @close_modal
    def form_valid(self, form: RoutineForm) -> Any:
        routine = self.get_routine()
        form.instance.routine = routine
        entry = form.save()
        messages.success(self.request, gettext("Entry created successfully"))
        return update_chart(
            custom_swap(
                EntryTableComponent.render_to_response(
                    kwargs={
                        "entries": [entry],
                    }
                ),
                "afterbegin",
                "#entry-table tbody",
                f'[data-entry-id="{entry.pk}"]',
            )
        )


class EntryUpdateView(LoginRequiredMixin, ModalFormMixin, UpdateView):
    model = RoutineEntry
    form_class = RoutineEntryForm
    template_name = "routines/entries/form.html"
    title = _("Update Entry")
    button_text = _("Save changes")

    def get_form_url(self) -> str:
        return reverse("routines:entry-edit-modal", kwargs={"pk": self.kwargs["pk"]})

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(routine__group__user=self.request.user)

    def get_success_url(self) -> str:
        return reverse("routines:group-detail", kwargs={"pk": self.get_object().routine.group.pk})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["routine"] = self.get_object().routine
        return context

    @close_modal
    def form_valid(self, form: RoutineEntryForm) -> Any:
        entry = form.save()
        selector = f'[data-entry-id="{entry.pk}"]'
        messages.success(self.request, gettext("Entry updated successfully"))

        return update_chart(
            custom_swap(
                EntryTableComponent.render_to_response(
                    kwargs={
                        "entries": [entry],
                    }
                ),
                "outerHTML",
                selector,
                selector,
            )
        )


class EntryDeleteView(LoginRequiredMixin, ModalDeleteMixin, DeleteView):
    model = RoutineEntry
    context_object_name = "entry"
    form_id = "delete-entry-form"
    title = _("Delete Entry")
    message = _("Are you sure you want to delete this entry?")

    def get_success_url(self) -> str:
        return reverse("routines:group-detail", kwargs={"pk": self.get_object().routine.group.pk})

    def get_callback(self) -> str:
        return f"deleteRoutineEntry({self.get_object().pk})"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(routine__group__user=self.request.user)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        response = super().post(request, *args, **kwargs)

        messages.success(request, gettext("Routine entry deleted successfully"))

        return update_chart(response)


class EntryTableView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        routine = get_object_or_404(Routine, pk=pk, group__user=request.user)

        try:
            page = int(request.GET.get("page", [1])[0])
        except ValueError:
            page = 1

        return EntryTableComponent.render_to_response(
            kwargs={
                "entries": routine.entries.all(),
                "page": page,
            }
        )


class EntryExportView(LoginRequiredMixin, View):
    export_formats = ["csv", "json"]
    field_names = ["date", "value", "notes"]

    def get_export_format(self, request: HttpRequest) -> str:
        export_format = request.GET.get("format", "csv")
        if export_format not in self.export_formats:
            export_format = "csv"

        return export_format

    def get_csv(self, response: HttpResponse, entries: List[RoutineEntry]) -> None:
        writer = csv.writer(response)
        writer.writerow(self.field_names)

        for obj in entries:
            writer.writerow([getattr(obj, field) for field in self.field_names])

    def get_json(self, response: HttpResponse, entries: List[RoutineEntry]) -> None:
        data = [{field: str(getattr(obj, field)) for field in self.field_names} for obj in entries]

        json.dump(data, response)

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        routine = get_object_or_404(Routine, pk=pk, group__user=request.user)
        entries = routine.entries.all()
        export_format = self.get_export_format(request)

        response = file_response(f"{routine.name}.{export_format}", f"text/{export_format}")

        if export_format == "csv":
            self.get_csv(response, entries)
        elif export_format == "json":
            self.get_json(response, entries)

        return response

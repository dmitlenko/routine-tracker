from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, UpdateView

from routine_tracker.base.mixins import ModalFormMixin
from routine_tracker.base.utils.htmx import custom_swap
from routine_tracker.base.utils.modal import close_modal
from routine_tracker.routines.components.entry_table.entry_table import EntryTableComponent

from ..forms import RoutineCreateForm, RoutineEntryForm
from ..models import Routine, RoutineEntry


class EntryCreateView(LoginRequiredMixin, ModalFormMixin, CreateView):
    model = RoutineEntry
    form_class = RoutineEntryForm
    template_name = 'routines/entries/form.html'
    title = _("Create Entry")
    button_text = _("Create")

    def get_routine(self) -> Routine:
        return get_object_or_404(Routine, pk=self.kwargs['pk'], group__user=self.request.user)

    def get_form_url(self) -> str:
        return reverse('routines:entry-create', kwargs={'pk': self.kwargs['pk']})

    def get_success_url(self) -> str:
        return reverse('routines:group-detail', kwargs={'pk': self.get_routine().group.pk})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['routine'] = get_object_or_404(Routine, pk=self.kwargs['pk'], group__user=self.request.user)
        return context

    def form_valid(self, form: RoutineCreateForm) -> Any:
        routine = self.get_routine()
        form.instance.routine = routine
        entry = form.save()
        messages.success(self.request, _("Entry created successfully"))
        return close_modal(
            custom_swap(
                EntryTableComponent.render_to_response(
                    kwargs={
                        'entries': [entry],
                    }
                ),
                'afterbegin',
                '#entry-table tbody',
                f'[data-entry-id="{entry.pk}"]',
            )
        )


class EntryUpdateView(LoginRequiredMixin, ModalFormMixin, UpdateView):
    model = RoutineEntry
    form_class = RoutineEntryForm
    template_name = 'routines/entries/form.html'
    title = _("Update Entry")
    button_text = _("Save changes")

    def get_form_url(self) -> str:
        return reverse('routines:entry-edit-modal', kwargs={'pk': self.kwargs['pk']})

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(routine__group__user=self.request.user)

    def get_success_url(self) -> str:
        return reverse('routines:group-detail', kwargs={'pk': self.get_object().routine.group.pk})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['routine'] = self.get_object().routine
        return context

    def form_valid(self, form: RoutineEntryForm) -> Any:
        entry = form.save()
        selector = f'[data-entry-id="{entry.pk}"]'
        messages.success(self.request, _("Entry updated successfully"))

        return close_modal(
            custom_swap(
                EntryTableComponent.render_to_response(
                    kwargs={
                        'entries': [entry],
                    }
                ),
                'outerHTML',
                selector,
                selector,
            )
        )


class EntryDeleteView(LoginRequiredMixin, ModalFormMixin, DeleteView):
    model = RoutineEntry
    template_name = 'routines/entries/confirm_delete.html'
    context_object_name = 'entry'

    def get_success_url(self) -> str:
        return reverse('routines:group-detail', kwargs={'pk': self.get_object().routine.group.pk})

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(routine__group__user=self.request.user)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        response = super().post(request, *args, **kwargs)
        response.status_code = 204

        messages.success(request, _("Routine entry deleted successfully"))

        return close_modal(response)

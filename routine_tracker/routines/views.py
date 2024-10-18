from datetime import date, timedelta
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from routine_tracker.base.mixins import ModalMixin
from routine_tracker.base.utils.htmx import forced_htmx_redirect

from .forms import RoutineCreateForm, RoutineEntryCreateForm, RoutineGroupCreateForm
from .models import Routine, RoutineEntry, RoutineGroup


class RoutineGroupListView(LoginRequiredMixin, ListView):
    model = RoutineGroup
    context_object_name = "groups"
    template_name = "routines/routine_group_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        start_date_str = self.request.GET.get('start', '')
        end_date_str = self.request.GET.get('end', '')

        start_date = date.fromisoformat(start_date_str) if start_date_str else date.today() - timedelta(days=7)
        end_date = date.fromisoformat(end_date_str) if end_date_str else None

        context.update(
            {
                'start': start_date,
                'end': end_date,
            }
        )

        return context

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(user=self.request.user).prefetch_related("routines")


class RoutineGroupDetailView(LoginRequiredMixin, DetailView):
    model = RoutineGroup
    context_object_name = "group"
    template_name = "routines/routine_group_detail.html"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(user=self.request.user).prefetch_related("routines")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["routines"] = context[self.context_object_name].routines.all()
        return context


class RoutineGroupCreateView(LoginRequiredMixin, ModalMixin, CreateView):
    model = RoutineGroup
    form_class = RoutineGroupCreateForm
    template_name = 'routines/routine_group_form.html'
    modal_options = {'backdrop': True}

    def get_success_url(self) -> str:
        return reverse('routines:group-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form: RoutineGroupCreateForm) -> Any:
        form.instance.user = self.request.user

        messages.success(self.request, "Routine group created successfully")

        return forced_htmx_redirect(super().form_valid(form), self.get_success_url(), 201)


class RoutineCreateView(LoginRequiredMixin, CreateView):
    model = Routine
    form_class = RoutineCreateForm
    template_name = 'routines/routine_form.html'

    def get_success_url(self) -> str:
        return reverse_lazy('routines:routine-group-detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form: RoutineCreateForm) -> Any:
        group = get_object_or_404(RoutineGroup, pk=self.kwargs['pk'], user=self.request.user)
        form.instance.group = group
        return super().form_valid(form)


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = RoutineEntry
    form_class = RoutineEntryCreateForm
    template_name = 'routines/entry_form.html'

    def get_success_url(self) -> str:
        return reverse_lazy('routines:routine-group-detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form: RoutineCreateForm) -> Any:
        routine = get_object_or_404(Routine, pk=self.kwargs['routine_id'], group__user=self.request.user)
        form.instance.routine = routine
        return super().form_valid(form)

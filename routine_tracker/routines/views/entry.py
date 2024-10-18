from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from ..forms import RoutineCreateForm, RoutineEntryCreateForm
from ..models import Routine, RoutineEntry


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

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from ..forms import RoutineCreateForm
from ..models import Routine, RoutineGroup


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

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import RoutineGroupCreateForm
from .models import RoutineGroup


class RoutineGroupListView(LoginRequiredMixin, ListView):
    model = RoutineGroup
    context_object_name = "groups"
    template_name = "routines/routine_group_list.html"

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


class RoutineGroupCreateView(LoginRequiredMixin, CreateView):
    model = RoutineGroup
    form_class = RoutineGroupCreateForm
    template_name = 'routines/routine_group_form.html'
    success_url = reverse_lazy('routines:routine-group-list')

    def form_valid(self, form: RoutineGroupCreateForm) -> Any:
        form.instance.user = self.request.user
        return super().form_valid(form)

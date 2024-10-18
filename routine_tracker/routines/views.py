from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from routine_tracker.base.mixins import ModalFormMixin, ModalMixin
from routine_tracker.base.utils.htmx import custom_swap, forced_htmx_redirect
from routine_tracker.routines.components.routine_group_item.routine_group_item import RoutineGroupItemComponent

from .forms import RoutineCreateForm, RoutineEntryCreateForm, RoutineGroupForm
from .models import Routine, RoutineEntry, RoutineGroup


class RoutineGroupListView(LoginRequiredMixin, ListView):
    model = RoutineGroup
    context_object_name = "groups"
    template_name = "routines/groups/list.html"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(user=self.request.user).prefetch_related("routines")


class RoutineGroupDetailView(LoginRequiredMixin, DetailView):
    model = RoutineGroup
    context_object_name = "group"
    template_name = "routines/groups/detail.html"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(user=self.request.user).prefetch_related("routines")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["routines"] = context[self.context_object_name].routines.all()
        return context


class RoutineGroupCreateView(LoginRequiredMixin, ModalFormMixin, CreateView):
    model = RoutineGroup
    form_class = RoutineGroupForm
    template_name = 'routines/groups/form.html'
    modal_options = {'backdrop': True}
    title = _('Create routine group')
    button_text = _('Create group')
    form_url = reverse_lazy('routines:group-create')
    extra_context = {'hx_swap': 'none'}

    def get_success_url(self) -> str:
        return reverse('routines:group-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form: RoutineGroupForm) -> Any:
        form.instance.user = self.request.user
        group = form.save()
        messages.success(self.request, _("Routine group created successfully"))
        response = RoutineGroupItemComponent.render_to_response(
            kwargs={
                'routine_group': group,
                'fade': True,
            }
        )

        return custom_swap(response, 'afterbegin', '#routine-group-list', '.routine-group-item', 201)


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


class RoutineGroupDeleteView(LoginRequiredMixin, ModalMixin, DeleteView):
    model = RoutineGroup
    template_name = 'routines/groups/confirm_delete.html'
    success_url = reverse_lazy('routines:group-list')
    context_object_name = 'group'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(user=self.request.user)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        response = super().post(request, *args, **kwargs)
        messages.success(request, _("Routine group deleted successfully"))

        if request.headers.get('HX-Origin') == 'detail':
            response = forced_htmx_redirect(
                response,
                reverse('routines:group-list'),
            )

        return response


class RoutineGroupUpdateView(LoginRequiredMixin, ModalFormMixin, UpdateView):
    model = RoutineGroup
    form_class = RoutineGroupForm
    template_name = 'routines/groups/form.html'
    context_object_name = 'group'
    success_url = reverse_lazy('routines:group-list')
    title = _('Edit routine group')
    button_text = _('Save changes')
    extra_context = {'hx_swap': 'outerHTML'}

    def get_form_url(self) -> str:
        return reverse('routines:group-edit-modal', kwargs={'pk': self.object.pk})

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form: RoutineGroupForm) -> Any:
        messages.success(
            self.request, _("Routine group '{group}' updated successfully").format(group=self.object.name)
        )
        form.save()
        response = RoutineGroupItemComponent.render_to_response(
            kwargs={
                'routine_group': self.get_object(),
                'fade': False,
            }
        )

        if self.request.headers.get('HX-Origin') == 'detail':
            return forced_htmx_redirect(
                response,
                reverse('routines:group-detail', kwargs={'pk': self.object.pk}),
            )

        return custom_swap(
            response,
            'outerHTML',
            f'[data-group-id="{self.object.pk}"]',
            '.routine-group-item',
        )

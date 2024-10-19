from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from routine_tracker.base.mixins import ModalFormMixin, ModalMixin
from routine_tracker.base.utils.htmx import custom_swap, forced_htmx_redirect
from routine_tracker.base.utils.modal import close_modal
from routine_tracker.routines.components.routine_group_item.routine_group_item import RoutineGroupItemComponent

from ..forms import RoutineGroupForm
from ..models import RoutineGroup


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

        return close_modal(
            custom_swap(
                response,
                'afterbegin',
                '#routine-group-list',
                '.routine-group-item',
                status_code=201,
            )
        )


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

        return close_modal(
            custom_swap(
                response,
                'outerHTML',
                f'[data-group-id="{self.object.pk}"]',
                '.routine-group-item',
            )
        )


class RoutineGroupDeleteView(LoginRequiredMixin, ModalMixin, DeleteView):
    model = RoutineGroup
    template_name = 'routines/groups/confirm_delete.html'
    success_url = reverse_lazy('routines:group-list')
    context_object_name = 'group'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(user=self.request.user)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        response = super().post(request, *args, **kwargs)
        response.status_code = 204

        messages.success(request, _("Routine group deleted successfully"))

        if request.headers.get('HX-Origin') == 'detail':
            response = forced_htmx_redirect(
                response,
                reverse('routines:group-list'),
            )

        return close_modal(response)

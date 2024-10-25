from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from routine_tracker.base.utils.htmx import custom_swap, htmx_redirect
from routine_tracker.base.utils.modal import close_modal
from routine_tracker.core.mixins import ModalDeleteMixin, ModalFormMixin
from routine_tracker.routines.components.routine_group.routine_group import RoutineGroupComponent
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
        messages.success(self.request, gettext("Routine group created successfully"))
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
        obj = form.save()
        messages.success(self.request, gettext("Routine group '{group}' updated successfully").format(group=obj.name))
        response = RoutineGroupItemComponent.render_to_response(
            kwargs={
                'routine_group': self.get_object(),
                'fade': False,
            }
        )

        if self.request.headers.get('HX-Origin') == 'detail':
            return close_modal(
                custom_swap(
                    RoutineGroupComponent.render_to_response(
                        kwargs={
                            'group': obj,
                        },
                    ),
                    'outerHTML',
                    '#routine-group-card',
                    '#routine-group-card',
                )
            )

        return close_modal(
            custom_swap(
                response,
                'outerHTML',
                f'[data-group-id="{obj.pk}"]',
                '.routine-group-item',
            )
        )


class RoutineGroupDeleteView(LoginRequiredMixin, ModalDeleteMixin, DeleteView):
    model = RoutineGroup
    context_object_name = 'group'
    form_id = 'delete-group-form'
    success_url = reverse_lazy('routines:group-list')
    title = _("Delete routine group")
    message = _("Are you sure you want to delete this routine group?")

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(user=self.request.user)

    def get_callback(self) -> str:
        return f'deleteRoutineGroup({self.get_object().pk})'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        response = super().post(request, *args, **kwargs)

        messages.success(request, gettext("Routine group deleted successfully"))

        if request.headers.get('HX-Origin') == 'detail':
            response = htmx_redirect(
                response,
                reverse('routines:group-list'),
            )

        return response

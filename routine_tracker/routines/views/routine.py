from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from routine_tracker.base.mixins import ModalFormMixin, ModalMixin
from routine_tracker.base.utils.htmx import custom_swap
from routine_tracker.base.utils.modal import close_modal
from routine_tracker.routines.components.routine_detail.routine_detail import RoutineDetailComponent
from routine_tracker.routines.components.routines.routines import RoutinesComponent

from ..forms import RoutineCreateForm
from ..models import Routine, RoutineGroup


class RoutineCreateView(LoginRequiredMixin, CreateView):
    model = Routine
    form_class = RoutineCreateForm
    template_name = 'routines/routines/form.html'
    extra_context = {
        'button_text': _('Create routine'),
    }

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form_url'] = reverse_lazy('routines:routine-create', kwargs={'pk': self.kwargs['pk']})
        return context

    def get_success_url(self, obj: Routine) -> str:
        return f"{reverse('routines:group-detail', kwargs={'pk': self.kwargs['pk']})}?routine={obj.pk}"

    def form_valid(self, form: RoutineCreateForm) -> Any:
        group = get_object_or_404(RoutineGroup, pk=self.kwargs['pk'], user=self.request.user)
        form.instance.group = group
        form.save()

        return custom_swap(
            RoutinesComponent.render_to_response(
                args=(group,),
                kwargs={
                    'request': self.request,
                    'current': form.instance,
                },
            ),
            'outerHTML',
            '#routines-card',
            '#routines-card',
            headers={'HX-Push-Url': self.get_success_url(form.instance)},
        )


class RoutineDetailView(LoginRequiredMixin, DetailView):
    model = Routine
    context_object_name = "routine"
    template_name = "routines/routines/detail.html"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(group__user=self.request.user)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return RoutineDetailComponent.render_to_response(
            context={'request': request},
            kwargs={
                'routine': self.get_object(),
            },
        )


class RoutineDeleteView(LoginRequiredMixin, ModalMixin, DeleteView):
    model = Routine
    template_name = 'routines/routines/confirm_delete.html'
    context_object_name = 'routine'

    def get_success_url(self) -> str:
        return reverse('routines:group-detail', kwargs={'pk': self.get_object().group.pk})

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(group__user=self.request.user)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        response = super().post(request, *args, **kwargs)
        response.status_code = 204

        messages.success(request, _("Routine group deleted successfully"))

        return close_modal(response)


class RoutineUpdateView(LoginRequiredMixin, ModalFormMixin, UpdateView):
    model = Routine
    form_class = RoutineCreateForm
    template_name = 'routines/routines/form_modal.html'
    context_object_name = 'routine'
    extra_context = {
        'button_text': _('Save changes'),
    }

    def get_form_url(self) -> str:
        return reverse('routines:routine-edit-modal', kwargs={'pk': self.object.pk, 'group_id': self.object.group.pk})

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(group__user=self.request.user)

    def form_valid(self, form: RoutineCreateForm) -> Any:
        messages.success(self.request, _("Routine '{routine}' updated successfully").format(routine=self.object.name))
        form.save()

        return close_modal(
            custom_swap(
                RoutinesComponent.render_to_response(
                    args=(self.object.group,),
                    kwargs={
                        'request': self.request,
                        'current': self.object,
                    },
                ),
                'outerHTML',
                '#routines-card',
                '#routines-card',
            )
        )

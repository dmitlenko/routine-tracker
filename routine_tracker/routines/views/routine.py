from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, View

from routine_tracker.base.utils.htmx import custom_swap
from routine_tracker.base.utils.modal import close_modal
from routine_tracker.core.mixins import ModalDeleteMixin, ModalFormMixin
from routine_tracker.core.utils.date import get_daterange
from routine_tracker.routines.components.routine_chart.routine_chart import RoutineChartComponent
from routine_tracker.routines.components.routine_detail.routine_detail import RoutineDetailComponent
from routine_tracker.routines.components.routines.routines import RoutinesComponent

from ..forms import RoutineForm
from ..models import Routine, RoutineGroup


class RoutineDetailView(LoginRequiredMixin, DetailView):
    model = Routine
    context_object_name = "routine"
    template_name = "routines/routines/detail.html"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(group__user=self.request.user)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return RoutineDetailComponent.render_to_response(
            context={"request": request},
            kwargs={
                "routine": self.get_object(),
            },
        )


class RoutineCreateView(LoginRequiredMixin, CreateView):
    model = Routine
    form_class = RoutineForm
    template_name = "routines/routines/form.html"
    extra_context = {
        "button_text": _("Create routine"),
        "measure_choices": Routine.DefaultMeasures.choices,
    }

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form_url"] = reverse_lazy("routines:routine-create", kwargs={"pk": self.kwargs["pk"]})
        return context

    def get_success_url(self, obj: Routine) -> str:
        return f"{reverse('routines:group-detail', kwargs={'pk': self.kwargs['pk']})}?routine={obj.pk}"

    def form_valid(self, form: RoutineForm) -> Any:
        group = get_object_or_404(RoutineGroup, pk=self.kwargs["pk"], user=self.request.user)
        form.instance.group = group
        form.save()

        return custom_swap(
            RoutinesComponent.render_to_response(
                context={"request": self.request},
                args=(group,),
                kwargs={
                    "request": self.request,
                    "current": form.instance,
                },
            ),
            "outerHTML",
            "#routines-card",
            "#routines-card",
            headers={"HX-Push-Url": self.get_success_url(form.instance)},
        )


class RoutineUpdateView(LoginRequiredMixin, ModalFormMixin, UpdateView):
    model = Routine
    form_class = RoutineForm
    template_name = "routines/routines/form_modal.html"
    context_object_name = "routine"
    extra_context = {
        "button_text": _("Save changes"),
        "measure_choices": Routine.DefaultMeasures.choices,
    }

    def get_form_url(self) -> str:
        return reverse("routines:routine-edit-modal", kwargs={"pk": self.object.pk})

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(group__user=self.request.user)

    @close_modal
    def form_valid(self, form: RoutineForm) -> Any:
        messages.success(
            self.request, gettext("Routine '{routine}' updated successfully").format(routine=self.object.name)
        )
        form.save()

        return custom_swap(
            RoutinesComponent.render_to_response(
                context={"request": self.request},
                args=(self.object.group,),
                kwargs={
                    "request": self.request,
                    "current": self.object,
                },
            ),
            "outerHTML",
            "#routines-card",
            "#routines-card",
        )


class RoutineDeleteView(LoginRequiredMixin, ModalDeleteMixin, DeleteView):
    model = Routine
    context_object_name = "routine"
    form_id = "delete-routine-form"
    title = _("Delete routine")
    message = _("Are you sure you want to delete this routine?")

    def get_success_url(self) -> str:
        return reverse("routines:group-detail", kwargs={"pk": self.get_object().group.pk})

    def get_callback(self) -> str:
        return f"$dispatch(`delete-routine`, {self.get_object().pk})"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(group__user=self.request.user)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        response = super().post(request, *args, **kwargs)

        messages.success(request, gettext("Routine group deleted successfully"))

        return response


class RoutineChartView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        routine = get_object_or_404(Routine, pk=pk, group__user=request.user)

        return RoutineChartComponent.render_to_response(
            kwargs={
                "routine": routine,
                "daterange": get_daterange(request),
            }
        )

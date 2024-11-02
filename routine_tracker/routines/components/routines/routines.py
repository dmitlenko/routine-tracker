from typing import Any, NotRequired, Optional, Tuple, TypedDict

from django.http import HttpRequest
from django_components import Component, register

from routine_tracker.routines.forms import RoutineForm
from routine_tracker.routines.models import Routine, RoutineGroup

Args = Tuple[RoutineGroup]


class Kwargs(TypedDict):
    request: NotRequired[Optional[HttpRequest]]
    current: NotRequired[Optional[Routine]]


@register("routines")
class RoutinesComponent(Component[Args, Kwargs, Any, Any]):
    template_name = "template.html"

    def get_request(self, request: Optional[HttpRequest]) -> HttpRequest:
        if request is None:
            return self.inject("request").request

        return request

    def get_context_data(
        self, group: RoutineGroup, *, request: Optional[HttpRequest] = None, current: Optional[Routine] = None
    ) -> Any:
        # Get the request object
        request = self.get_request(request)

        # Get the routines for the group
        routines = group.routines.all()

        # Try to get the current routine from the request
        routine_id = request.GET.get("routine")

        # If a routine is not specified in the request, try to get the current routine from the component
        if current:
            current_routine = current
        elif routine_id:
            try:
                current_routine = group.routines.get(pk=routine_id)
            except Routine.DoesNotExist:
                # If the routine specified in the request does not exist, default to the first routine
                current_routine = routines.first()
        else:
            current_routine = routines.first()

        return {
            "group": group,
            "routines": routines,
            "current_routine": current_routine,
            "form": RoutineForm,
        }

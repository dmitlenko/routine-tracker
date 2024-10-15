from typing import Any, TypedDict, Unpack

from django_components import Component, register

from routine_tracker.routines.models import RoutineGroup


class Kwargs(TypedDict):
    group: RoutineGroup


@register('routine_group')
class RoutineGroupComponent(Component):
    template_name = 'routine_group.html'

    def get_context_data(self, *_: Any, **kwargs: Unpack[Kwargs]) -> Any:
        group = kwargs['group']
        routines = group.routines.all()[:3]

        return {
            'group': group,
            'routines': routines,
        }

from typing import Any

from django_components import Component, register

from routine_tracker.routines.models import RoutineGroup


@register('routine-group')
class RoutineGroupComponent(Component):
    template_name = 'template.html'

    def get_context_data(self, group: RoutineGroup) -> Any:
        return {'group': group}

    class Media:
        js = 'script.js'

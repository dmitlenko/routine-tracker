from typing import Any, List

from django_components import Component, register

from routine_tracker.routines.models import Routine, RoutineEntry


@register('routine-detail')
class RoutineDetailComponent(Component):
    template_name = 'template.html'

    def get_context_data(self, routine: Routine) -> Any:
        entries: List[RoutineEntry] = routine.entries.all()

        return {
            'routine': routine,
            'entries': entries,
        }

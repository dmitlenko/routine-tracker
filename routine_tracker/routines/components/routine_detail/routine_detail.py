from typing import Any

from django_components import Component, register

from routine_tracker.routines.models import Routine


@register('routine-detail')
class RoutineDetailComponent(Component):
    template_name = 'template.html'

    def get_context_data(self, routine: Routine) -> Any:
        return {
            'routine': routine,
            'entries': routine.entries.all(),
        }

    class Media:
        js = 'script.js'

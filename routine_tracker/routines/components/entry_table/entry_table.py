from typing import Any, List

from django_components import Component, register

from routine_tracker.routines.models import RoutineEntry


@register('entry-table')
class EntryTableComponent(Component):
    template_name = 'template.html'

    def get_context_data(self, entries: List[RoutineEntry]) -> Any:
        return {'entries': entries}

    class Media:
        js = 'script.js'

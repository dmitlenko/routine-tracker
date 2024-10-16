from typing import TypedDict, Unpack

from django_components import Component, register

from routine_tracker.routines.models import Routine


class Kwargs(TypedDict):
    routine: Routine


@register('routine')
class RoutineComponent(Component):
    template_name = 'routine.html'

    def get_context_data(self, *_: None, **kwargs: Unpack[Kwargs]) -> Kwargs:
        routine = kwargs['routine']
        entries = routine.entries.all()

        return {
            'routine': routine,
            'entries': entries,
        }

    class Media:
        css = 'style.css'

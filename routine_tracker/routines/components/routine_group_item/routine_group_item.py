from typing import Any, TypedDict, Union, Unpack

from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _
from django_components import Component, register

from routine_tracker.routines.models import RoutineGroup


class Kwargs(TypedDict):
    routine_group: RoutineGroup
    fade: Union[str, bool]


@register('routine_group_item')
class RoutineGroupItemComponent(Component[Any, Kwargs, Any, Any]):
    template_name = 'template.html'

    def lastupdated(self, value: RoutineGroup) -> str:
        if value.routines.exists():
            entry = value.get_latest_entry()

            if entry:
                return _('Last updated {date} ago').format(date=timesince(entry.date))

        return _('Never updated')

    def get_context_data(self, **kwargs: Unpack[Kwargs]) -> Kwargs:
        fade = kwargs['fade']
        fade = fade if isinstance(fade, bool) else fade == 'true'

        return {
            'group': kwargs['routine_group'],
            'fade': fade,
            'lastupdated': self.lastupdated(kwargs['routine_group']),
        }

    class Media:
        js = 'script.js'

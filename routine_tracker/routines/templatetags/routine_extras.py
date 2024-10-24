import json
from datetime import datetime
from typing import Union

from django import template

from routine_tracker.routines.models import Routine, RoutineEntry

register = template.Library()


@register.filter
def duration(value: int) -> str:
    dt = datetime.fromtimestamp(value)

    if dt.hour == 0:
        return dt.strftime("%M:%S")

    return dt.strftime("%H:%M:%S")


@register.simple_tag
def time_entry_data(obj: Union[RoutineEntry, Routine, None] = None) -> str:
    value = 0

    if isinstance(obj, Routine):
        value = obj.goal or 0
    elif isinstance(obj, RoutineEntry):
        value = obj.value or 0
    elif obj is None:
        pass
    else:
        raise ValueError("obj must be an instance of Routine or RoutineEntry")

    dt = datetime.fromtimestamp(value)

    return json.dumps(
        {
            "hours": dt.hour,
            "minutes": dt.minute,
            "seconds": dt.second,
        }
    )

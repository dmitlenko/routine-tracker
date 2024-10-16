from datetime import date, datetime
from typing import Union

from django import template

from routine_tracker.routines.models import Routine, RoutineGroup, RoutineGroupStatistics, RoutineStatistics

register = template.Library()


@register.filter
def duration(value: int) -> str:
    dt = datetime.fromtimestamp(value)

    if dt.hour == 0:
        return dt.strftime("%M:%S")

    return dt.strftime("%H:%M:%S")


@register.simple_tag
def statistics(
    *, obj: Union[Routine, RoutineGroup], start: date, end: date = None
) -> Union[RoutineStatistics, RoutineGroupStatistics]:
    if not isinstance(obj, (Routine, RoutineGroup)):
        raise ValueError("obj must be an instance of Routine or RoutineGroup")

    if (stats := obj.statistics(start, end)) is not None:
        return stats[0]

    return None

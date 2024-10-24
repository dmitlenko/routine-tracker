from typing import List, TypedDict, Union

from django.db import models
from django.utils.translation import gettext as _

from routine_tracker.core.utils.chart import ChartOptions, chart
from routine_tracker.core.utils.date import daterange
from routine_tracker.routines.models import Routine, RoutineEntry, RoutineGroup


def routine_statistics_chart(routine: Routine, range: daterange) -> Union[ChartOptions, None]:
    entries: List[RoutineEntry] = routine.entries.filter(date__in=range)
    line_tension = 0.1
    padding = 10

    if not entries:
        return None

    entry_dict = {entry.date: entry.value for entry in entries}
    data = [entry_dict.get(date, None) for date in range]

    max_value = max(filter(None, data))
    min_value = min(filter(None, data))
    average = sum(filter(None, data)) / len(entries)

    chrt = chart(
        {
            'type': 'line',
            'data': {
                'labels': [date.strftime('%Y-%m-%d') for date in range],
                'datasets': [
                    {
                        'label': _('Value'),
                        # Data is a list of values for each date in the range
                        # If there is no entry for a date, the value is None
                        'data': data,
                        'fill': True,
                        'borderColor': 'rgb(75, 192, 192)',
                        'lineTension': line_tension,
                    },
                    {
                        'label': _('Average'),
                        'data': [average] + [None] * (len(range) - 2) + [average],
                        'fill': False,
                        'borderColor': 'rgb(54, 162, 235)',
                        'lineTension': line_tension,
                    },
                ],
            },
            'options': {
                'spanGaps': True,
                'scales': {
                    'y': {
                        'min': min_value - padding if min_value > 1 else 0,
                        'max': max_value + padding,
                    },
                },
            },
        }
    )

    if routine.has_goal:
        chrt['options']['scales']['y']['max'] = max(routine.goal, max_value) + padding
        chrt['data']['datasets'].append(
            {
                'label': _('Goal'),
                'data': [routine.goal] + [None] * (len(range) - 2) + [routine.goal],
                'fill': False,
                'borderColor': 'rgb(255, 99, 132)',
            }
        )

    return chrt


class RoutineGroupStatistics(TypedDict):
    total_routines: int
    total_entries: int
    most_entries: Routine
    average_value: float


def routine_group_statistics(group: RoutineGroup) -> RoutineGroupStatistics:
    total_routines = group.routines.count()
    total_entries = RoutineEntry.objects.filter(routine__group=group).count()
    most_entries = group.routines.annotate(entry_count=models.Count('entries')).order_by('-entry_count').first()
    average_value = RoutineEntry.objects.filter(routine__group=group).aggregate(models.Avg('value'))['value__avg']

    return {
        'total_routines': total_routines,
        'total_entries': total_entries,
        'most_entries': most_entries,
        'average_value': round(average_value, 2) if average_value else 0,
    }

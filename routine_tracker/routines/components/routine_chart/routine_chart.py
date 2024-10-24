from typing import Any

from django_components import Component, register

from routine_tracker.core.utils.date import daterange, get_daterange
from routine_tracker.routines.models import Routine
from routine_tracker.routines.utils.statistics import routine_statistics_chart


@register("routine-chart")
class RoutineChartComponent(Component):
    template_name = "template.html"

    def get_context_data(self, routine: Routine, daterange: daterange = None) -> Any:
        if not daterange:
            daterange = get_daterange(self.inject('request').request)

        chart = routine_statistics_chart(routine, daterange)

        return {
            'chart': chart,
        }

import json
from typing import Any

from django.urls import reverse
from django_components import Component, register

from routine_tracker.core.utils.date import get_daterange


@register("statistics-range")
class StatisticsRangeComponent(Component):
    template_name = "template.html"

    def get_context_data(self, chart_reverse: str, **kwargs) -> Any:
        daterange = get_daterange(self.inject('request').request)

        if not kwargs.get('id'):
            raise ValueError('id is required')

        return {
            'class': kwargs.pop('class', ''),
            'start': daterange.start,
            'end': daterange.end,
            'component_settings': json.dumps(
                {
                    'chartUrl': reverse(chart_reverse, kwargs=kwargs.get('url', {})),
                    'chartId': kwargs['id'],
                }
            ),
        }

    class Media:
        js = 'script.js'

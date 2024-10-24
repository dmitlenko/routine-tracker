import json
from typing import Dict

from django.template import Library
from django_components.attributes import attributes_to_string

from routine_tracker.core.utils.chart import ChartOptions

register = Library()


@register.inclusion_tag("core/chart.html")
def render_chart(chart: ChartOptions, **kwargs) -> Dict:
    # Get the id from the kwargs
    _id = kwargs.get("id", None)

    # Check if id is provided
    if not _id:
        # If id is not provided, raise an error
        raise ValueError("You must provide an id for the chart")

    return {
        "id": _id,
        "chart": json.dumps(chart),
        "attrs": attributes_to_string(kwargs),
    }

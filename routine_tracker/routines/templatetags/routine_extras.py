from datetime import datetime

from django import template

register = template.Library()


@register.filter
def duration(value: int) -> str:
    dt = datetime.fromtimestamp(value)

    if dt.hour == 0:
        return dt.strftime("%M:%S")

    return dt.strftime("%H:%M:%S")

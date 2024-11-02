import json

from django.template import Library

register = Library()


@register.simple_tag
def fieldbind(field):
    params = json.dumps(
        {
            "field": field.name,
            "errors": list(map(str, field.errors)),
        }
    )

    return params


@register.filter
def isfieldtype(field, type) -> bool:
    if hasattr(field.field.widget, "input_type"):
        return field.field.widget.input_type == type

    return False

from django import template

register = template.Library()


@register.filter
def isfieldtype(field, type) -> bool:
    if hasattr(field.field.widget, "input_type"):
        return field.field.widget.input_type == type

    return False

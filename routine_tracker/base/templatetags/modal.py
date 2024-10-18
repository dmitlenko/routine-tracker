from django import template
from django.urls import reverse
from django_components.attributes import attributes_to_string

register = template.Library()


@register.simple_tag
def hxmodal(url: str) -> str:
    """Generates attribtues for htmx modal trigger

    Args:
        url (str): Reverse url name to fetch modal content

    Example:
        `<a {% hxmodal 'app_name:create-modal' %}>Create Group</a>`

    Returns:
        str: Attributes string

    """

    return attributes_to_string(
        {
            'hx-get': reverse(url),
            'hx-swap-oob': 'true',
            'hx-target': '#modalContainer',
            'hx-swap': 'innerHTML',
        }
    )

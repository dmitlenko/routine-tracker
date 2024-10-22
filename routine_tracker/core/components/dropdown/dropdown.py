from typing import Any, Dict, Unpack

from django_components import Component, register
from django_components.attributes import attributes_to_string


@register('dropdown')
class DropdownComponent(Component):
    template_name = 'template.html'

    def get_context_data(self, **kwargs: Unpack[Dict[str, Any]]) -> Any:
        classes = kwargs.pop('class', '')

        return {
            'class': classes,
            'attrs': attributes_to_string(kwargs),
        }

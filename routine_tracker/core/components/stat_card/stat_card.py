from typing import Any

from django_components import Component, register
from django_components.attributes import attributes_to_string


@register('stat-card')
class StatCardComponent(Component):
    template_name = 'template.html'

    def get_context_data(
        self, value: Any, description: str, icon: str, color: str = 'primary', horizontal: bool = False, **kwargs
    ) -> dict:
        return {
            'value': value,
            'description': description,
            'icon': icon,
            'color': color,
            'horizontal': horizontal,
            'class': kwargs.pop('class', ''),
            'attrs': attributes_to_string(kwargs),
        }

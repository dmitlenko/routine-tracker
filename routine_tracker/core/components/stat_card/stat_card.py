from typing import Any

from django_components import Component, register


@register('stat-card')
class StatCardComponent(Component):
    template_name = 'template.html'

    def get_context_data(self, value: Any, description: str, icon: str, color: str = 'primary') -> dict:
        return {
            'value': value,
            'description': description,
            'icon': icon,
            'color': color,
        }

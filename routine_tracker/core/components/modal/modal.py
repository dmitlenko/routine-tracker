from typing import Any

from django_components import Component, register
from django_components.attributes import attributes_to_string


@register('modal')
class ModalComponent(Component):
    template_name = 'modal.html'

    def get_context_data(self, title: str = '', **kwargs) -> Any:
        return {
            'title': title,
            'modal_attrs': attributes_to_string(kwargs) if kwargs else '',
        }

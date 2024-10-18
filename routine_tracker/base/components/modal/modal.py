from typing import Any

from django_components import Component, register


@register('modal')
class ModalComponent(Component):
    template_name = 'modal.html'

    def get_context_data(self, id: str, title: str = '') -> Any:
        return {'title': title, 'id': id}

from typing import Dict

from django.forms import Form
from django_components import Component, register
from django_components.attributes import attributes_to_string


@register('form')
class FormComponent(Component):
    template_name = 'template.html'

    def get_context_data(
        self,
        form: Form,
        *,
        horizontal: bool = False,
        horizontal_labels: bool = False,
        cols: int = 2,
        attrs: str = '',
        **kwargs,
    ) -> Dict:
        return {
            'form': form,
            'horizontal': horizontal,
            'horizontal_labels': horizontal_labels,
            'grid_style': f'grid-template-columns: repeat({cols}, 1fr);' if cols else '',
            'cols': cols,
            'attrs': attrs,
            'form_attrs': attributes_to_string(kwargs) if kwargs else '',
        }

from typing import Dict

from django.forms import Form
from django_components import Component, register
from django_components.attributes import attributes_to_string


@register('form')
class FormComponent(Component):
    template_name = 'template.html'

    def get_context_data(self, form: Form, *, horizontal: str = '', boost: str = '', **kwargs) -> Dict:
        return {
            'form': form,
            'horizontal': horizontal == 'true',
            'boost': boost == 'true',
            'form_attrs': attributes_to_string(kwargs),
        }

    class Media:
        js = 'script.js'
from typing import Any

from django_components import Component, register
from django_components.attributes import attributes_to_string


@register('form-controls')
class FormControlsComponent(Component):
    template_name = 'template.html'

    def get_context_data(
        self,
        form_id: str = '',
        wrap: bool = False,
        submit_text: str = "Submit",
        dismiss_text: str = "Cancel",
        in_modal: bool = False,
        **kwargs,
    ) -> Any:
        return {
            'wrap': wrap,
            'form_id': attributes_to_string({'form': form_id}) if form_id else '',
            'submit_text': submit_text,
            'dismiss_text': dismiss_text,
            'in_modal': attributes_to_string({'data-bs-dismiss': 'modal'}) if in_modal else '',
            'attrs': attributes_to_string(kwargs) if kwargs else '',
        }

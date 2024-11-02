from typing import Any

from django_components import Component, register
from django_components.attributes import attributes_to_string


@register("loader")
class LoaderComponent(Component):
    template_name = "template.html"

    def get_context_data(self, **kwargs) -> Any:
        return {"attrs": attributes_to_string(kwargs)}

    class Media:
        css = "styles.css"

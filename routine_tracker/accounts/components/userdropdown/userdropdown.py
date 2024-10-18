from typing import Any

from django.http import HttpRequest
from django_components import Component, register


@register('userdropdown')
class UserDropdownComponent(Component):
    template_name = 'userdropdown.html'

    def get_context_data(self, *args: Any, **kwargs: Any) -> Any:
        request: HttpRequest = self.inject('request').request

        return {'user': request.user}

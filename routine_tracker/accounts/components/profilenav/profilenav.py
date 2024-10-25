from typing import Any

from django.utils.translation import gettext_lazy as _
from django_components import Component, register
from django_components.attributes import attributes_to_string

from routine_tracker.base.utils.nav import lks


@register('profilenav')
class ProfileNavComponent(Component):
    template_name = 'profilenav.html'

    def get_context_data(self, *args: Any, **kwargs: Any) -> Any:
        return {
            'navlinks': lks(
                ('accounts:profile', _('Profile')),
                ('accounts:settings', _('Settings')),
            ).reverse(self.inject('request').request),
            'attrs': attributes_to_string(kwargs),
        }

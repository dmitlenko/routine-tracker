from dataclasses import dataclass
from typing import Any, Literal, TypedDict, Union, Unpack

from django.http import HttpRequest
from django.urls import reverse
from django_components import Component, register


@dataclass
class NavbarLink:
    reverse_name: str
    text: str

    url: str = '#'
    active: Union[Literal[''], Literal["active"]] = None


class Kwargs(TypedDict):
    request: HttpRequest


NAVLINKS = [
    NavbarLink('base:index', 'Home'),
    NavbarLink('routines:routine-group-list', 'Routines'),
]


@register('navbar')
class NavbarComponent(Component):
    template_name = 'navbar.html'

    def get_context_data(self, *args: Any, **kwargs: Unpack[Kwargs]) -> Any:
        # Get the request object from the kwargs
        request: HttpRequest = self.inject('request').request

        # Create a copy of the navlinks list
        navlinks = NAVLINKS.copy()

        # Loop through the navlinks list and set the active attribute
        for link in navlinks:
            # Check if the current view name matches the reverse_name of the link
            is_active = request.resolver_match.view_name == link.reverse_name

            # Set the active attribute to 'active' if the link is active
            link.active = 'active' if is_active else ''

            # Set the url of the link to the reverse_name if the link is not active
            if is_active:
                link.url = '#'
            else:
                link.url = reverse(link.reverse_name)

        return {
            'navlinks': navlinks,
        }

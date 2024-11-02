from dataclasses import dataclass
from typing import List, Literal, Tuple, Union

from django.http import HttpRequest
from django.urls import reverse


@dataclass
class Link:
    reverse_name: str
    text: str

    url: Union[Literal["#"], str] = "#"
    active: Union[Literal[""], Literal["active"]] = None


class LinkHolder:
    def __init__(self, *initial_links: List[Link]):
        self.links = list(initial_links)

    def add(self, reverse_name: str, text: str):
        self.links.append(Link(reverse_name, text))

    def get(self):
        return self.links

    def reverse(self, request: HttpRequest) -> List[Link]:
        # Create a copy of the navlinks list
        navlinks = self.links.copy()

        # Loop through the navlinks list and set the active attribute
        for link in navlinks:
            # Check if the current view name matches the reverse_name of the link
            is_active = request.resolver_match.view_name == link.reverse_name

            # Set the active attribute to 'active' if the link is active
            link.active = "active" if is_active else ""

            # Set the url of the link to the reverse_name if the link is not active
            if is_active:
                link.url = "#"
            else:
                link.url = reverse(link.reverse_name)

        return navlinks


def lks(*links: List[Tuple[str, str]]) -> LinkHolder:
    """Short hand function to create a LinkHolder object with multiple links

    Returns:
        LinkHolder: A LinkHolder object with multiple links
    """

    return LinkHolder(*[Link(*link) for link in links])

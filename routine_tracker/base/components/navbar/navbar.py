from typing import Any

from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django_components import Component, register

from routine_tracker.base.utils.nav import lks

links = lks(
    ("base:index", _("Dashboard")),
    ("routines:group-list", _("Routine Groups")),
)


@register("navbar")
class NavbarComponent(Component):
    template_name = "navbar.html"

    def get_context_data(self, *args: Any, **kwargs: Any) -> Any:
        # Get the request object from the kwargs
        request: HttpRequest = self.inject("request").request

        # If user is not authenticated, return the context with is_authenticated set to false
        if not request.user.is_authenticated:
            return {"is_authenticated": False}

        return {
            "navlinks": links.reverse(request),
            "is_authenticated": True,
        }

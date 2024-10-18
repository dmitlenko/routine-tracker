from typing import Literal, Optional, TypedDict, Union

from django.http import HttpResponse
from django_htmx.http import trigger_client_event


class ModalOptions(TypedDict):
    backdrop: Optional[Union[bool, Literal['static']]]
    focus: Optional[bool]
    keyboard: Optional[bool]


def trigger_modal(response: HttpResponse, options: ModalOptions = None):
    """Triggers a modal to show

    Args:
        response (HttpResponse): Response object
        options (ModalOptions, optional): Modal options. Defaults to None.

    Returns:
        HttpResponse: Response object
    """
    options = options or {}

    return trigger_client_event(response, 'hx-show-modal', options)

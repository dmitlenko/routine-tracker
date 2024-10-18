from typing import Any, Literal, Optional, TypedDict, Union, Unpack

from django.http import HttpResponse
from django_htmx.http import trigger_client_event


class ModalOptions(TypedDict):
    backdrop: Optional[Union[bool, Literal['static']]]
    focus: Optional[bool]
    keyboard: Optional[bool]


def modal_options(id: str, **kwargs: Unpack[ModalOptions]) -> dict[str, Any]:
    """Generates modal options
    Refer to https://getbootstrap.com/docs/5.3/components/modal/#via-javascript for more info

    Args:
        backdrop (Union[bool, Literal['static']], optional): Includes a modal-backdrop element. Alternatively, specify
        static for a backdrop which doesn’t close the modal when clicked.

        focus (bool, optional): Puts the focus on the modal when initialized. Defaults to True.
        keyboard (bool, optional): 	Closes the modal when escape key is pressed. Defaults to True.

    Returns:
        dict[str, Any]: Modal options
    """

    return {
        'id': id,
        'options': {
            'backdrop': kwargs.get('backdrop', 'static'),
            'focus': kwargs.get('focus', True),
            'keyboard': kwargs.get('keyboard', True),
        },
    }


def trigger_modal(response: HttpResponse, modal_id: str = "modal", options: ModalOptions = None):
    """Triggers a modal to show

    Args:
        response (HttpResponse): Response object
        modal_id (str, optional): Modal ID. Defaults to "modal".
        options (ModalOptions, optional): Modal options. Defaults to None.

    Returns:
        HttpResponse: Response object
    """
    options = options or {}

    return trigger_client_event(response, 'hx-show-modal', modal_options(modal_id, **options))

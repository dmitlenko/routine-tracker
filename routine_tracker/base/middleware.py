from typing import Callable

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django_htmx.http import trigger_client_event


def message_middleware(get_response: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    def middleware(request: HttpRequest) -> HttpResponse:
        # Get the response
        response = get_response(request)

        # Ignore non-htmx requests
        if not request.htmx:
            return response

        # Ignore redirect responses
        if 300 <= response.status_code < 400:
            return response

        # Get request messages
        messages_ = messages.get_messages(request)

        # Trigger the event only if response contains messages
        if len(messages_) > 0:
            response = trigger_client_event(
                response,
                'hx-show-message',
                {
                    'messages': [
                        {
                            'tags': message.tags,
                            'message': message.message,
                        }
                        for message in messages_
                    ]
                },
            )

        # Return the response
        return response

    return middleware

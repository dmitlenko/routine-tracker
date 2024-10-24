from typing import Callable
from urllib.parse import parse_qs

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

        # Ignore if response is not successful
        if not 200 <= response.status_code < 300:
            return response

        # Ignore if response contains redirect or refresh headers
        if response.has_header('HX-Redirect') or response.has_header('HX-Refresh'):
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


def query_params_middleware(get_resonse: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    allowed_query_params = ('from', 'to', 'page', 'routine')

    def middlware(request: HttpRequest):
        if not request.htmx:
            return get_resonse(request)

        query_params = parse_qs(request.headers['HX-Current-URL'].split('?')[-1])
        query_params = {
            key: value[0] if len(value) == 1 else value
            for key, value in query_params.items()
            if key in allowed_query_params
        }

        request.GET = {
            **query_params,
            **request.GET,
        }

        return get_resonse(request)

    return middlware

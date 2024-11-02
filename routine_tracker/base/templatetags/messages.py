from django import template
from django.contrib import messages
from django.http import HttpRequest

register = template.Library()


@register.simple_tag
def messages_to_json(request: HttpRequest) -> dict[str, list[dict[str, str]]]:
    return {
        "messages": [
            {
                "tags": message.tags,
                "message": message.message,
            }
            for message in messages.get_messages(request)
        ]
    }

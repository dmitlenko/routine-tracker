from django.http import HttpResponse
from django_htmx.http import trigger_client_event


def update_chart(response: HttpResponse) -> HttpResponse:
    return trigger_client_event(response, 'hx-chart-update')

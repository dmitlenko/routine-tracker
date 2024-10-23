from typing import Any, List

from django.core.paginator import Paginator
from django.urls import reverse
from django_components import Component, register

from routine_tracker.routines.models import RoutineEntry


@register('entry-table')
class EntryTableComponent(Component):
    template_name = 'template.html'

    def get_context_data(self, entries: List[RoutineEntry], page: int = 1) -> Any:
        pages = Paginator(entries, 10)
        page_obj = pages.page(page)

        next_page = page_obj.next_page_number() if page_obj.has_next() else None

        if next_page:
            next_page_url = reverse('routines:entry-table', kwargs={'pk': entries.first().routine.pk})

            last_obj = {
                'hx-trigger': 'intersect once',
                'hx-target': '#entry-table tbody',
                'hx-select': '#entry-table tbody tr',
                'hx-get': f'{next_page_url}?page={next_page}',
                'hx-swap': 'beforeend',
            }
        else:
            last_obj = {}

        return {'entries': page_obj.object_list, 'page': page_obj, 'last': last_obj}

    class Media:
        js = 'script.js'

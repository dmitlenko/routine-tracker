import json
from typing import Any, List, Tuple

from django.urls import reverse
from django_components import Component, register

from routine_tracker.routines.models import Routine, RoutineGroup


@register('routines-nav')
class RoutinesNavigationComponent(Component):
    template_name = 'template.html'

    def get_data(self) -> Tuple[RoutineGroup, List[Routine], Routine]:
        data = self.inject('routine_data')
        group = data.group
        routines = group.routines.all()
        current = self.inject('routine_data').current

        return group, routines, current

    def get_context_data(
        self,
        group: RoutineGroup,
        routines: List[Routine],
        current: Routine,
        loader_id: str = "loader",
        target: str = "routines-card-body",
    ) -> Any:
        return {
            'group': group,
            'routines': [
                {
                    'obj': routine,
                    'attrs': json.dumps(
                        {
                            'pk': routine.pk,
                            'get': reverse(
                                'routines:routine-detail',
                                kwargs={'pk': routine.pk},
                            ),
                            'push': f'{reverse("routines:group-detail", kwargs={"pk": group.pk})}?routine={routine.pk}',
                        }
                    ),
                }
                for routine in routines
            ],
            'component_settings': json.dumps(
                {
                    'initialId': current.pk if current else -1,
                    'loaderId': loader_id,
                    'targetId': target,
                }
            ),
        }

    class Media:
        js = 'script.js'

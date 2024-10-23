from django_components import Component, register

from routine_tracker.routines.models import RoutineGroup
from routine_tracker.routines.utils import routine_group_statistics


@register("group-stats")
class GroupStatsComponent(Component):
    template_name = "template.html"

    def get_context_data(self, group: RoutineGroup) -> dict:
        return routine_group_statistics(group)

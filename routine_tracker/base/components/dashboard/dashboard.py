from datetime import datetime, timedelta
from typing import Any, Tuple, Union

from django.db.models import Count, QuerySet
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from django_components import Component, register

from routine_tracker.accounts.models import User
from routine_tracker.core.utils.chart import ChartData, chart
from routine_tracker.core.utils.date import get_default_daterange
from routine_tracker.routines.models import Routine, RoutineEntry, RoutineGroup
from routine_tracker.routines.utils.statistics import routine_statistics_chart


@register('dashboard')
class DashboardComponent(Component):
    template_name = 'template.html'

    def get_user_data(self, user: User) -> Tuple[QuerySet[RoutineGroup], QuerySet[Routine]]:
        groups = user.routine_groups.all()
        routines = Routine.objects.filter(group__in=groups)
        return groups, routines

    def get_latest_routine(self, routines: QuerySet[Routine]) -> Union[Routine, None]:
        entry = RoutineEntry.objects.filter(routine__in=routines)
        if entry.exists():
            return entry.latest('date').routine
        return None

    def get_last_entries(self, routines: QuerySet[Routine], count: int = 5) -> QuerySet[RoutineEntry]:
        return RoutineEntry.objects.filter(routine__id__in=routines.values_list('id'))[:count]

    def get_streak(self, routines: QuerySet[Routine]) -> str:
        entries = (
            RoutineEntry.objects.filter(routine__in=routines)
            .values('date')
            .annotate(dcount=Count('date'))
            .order_by('-date')
        )

        sequentrial_entries = []
        previous_date = None

        for entry in entries:
            if previous_date is None or entry['date'] == previous_date - timedelta(days=1):
                sequentrial_entries.append(entry)
                previous_date = entry['date']
            else:
                # The streak is broken
                break

        # break streak if the last entry is not today
        if sequentrial_entries and sequentrial_entries[0]['date'] != datetime.now().date():
            return 0

        streak = len(sequentrial_entries)

        if not streak:
            return _('No streak')

        return ngettext('{days} day', '{days} days', streak).format(days=streak)

    def get_groups_entries_chart(self, groups: QuerySet[RoutineGroup]) -> Tuple[ChartData, bool]:
        values = groups.values('name', 'color').annotate(entries=Count('routines__entries'))

        chrt = chart(
            {
                'type': 'doughnut',
                'data': {
                    'labels': [value['name'] for value in values],
                    'datasets': [
                        {
                            'label': _('Entries'),
                            'data': [value['entries'] for value in values],
                            'backgroundColor': [value['color'] for value in values],
                            'hoverOffset': 4,
                        },
                    ],
                },
            }
        )

        show = sum([value['entries'] for value in values]) > 0

        return chrt, show

    def get_top_routines(self, routines: QuerySet[Routine], count: int = 5) -> QuerySet[Routine]:
        return [
            {
                'routine': routine,
                'entry_count': ngettext('{count} entry', '{count} entries', routine.entry_count).format(
                    count=routine.entry_count
                ),
            }
            for routine in routines.annotate(entry_count=Count('entries')).order_by('-entry_count')[:count]
        ]

    def get_context_data(self, user: User) -> Any:
        groups, routines = self.get_user_data(user)
        latest_routine = self.get_latest_routine(routines)
        last_entries = self.get_last_entries(routines)
        streak = self.get_streak(routines)
        lr_chart = routine_statistics_chart(latest_routine, get_default_daterange()) if latest_routine else None
        entries_chart, show_entries_chart = self.get_groups_entries_chart(groups)
        top_routines = self.get_top_routines(routines)
        new_user = False

        if not groups.exists():
            new_user = True

        return {
            'new_user': new_user,
            'groups': groups[:3],
            'total_groups': groups.count(),
            'routines': routines,
            'latest_routine': latest_routine,
            'lr_chart': lr_chart,
            'last_entries': last_entries,
            'streak': streak,
            'entries_chart': entries_chart,
            'show_entries_chart': show_entries_chart,
            'top_routines': top_routines,
        }

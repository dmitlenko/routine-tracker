from datetime import date, timedelta
from typing import Dict, Tuple, TypedDict, Union

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


StreakStatistics = TypedDict(
    'StreakStatistics',
    {
        'completeness': float,
        'days': int,
        'start': date,
        'end': date,
        'missed': int,
    },
)


RoutineStatistics = TypedDict(
    'RoutineStatistics',
    {
        'total': int,
        'completed': int,
        'average': float,
        'best': int,
        'worst': int,
        'streak': StreakStatistics,
    },
)


class RoutineGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='routine_groups')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name


class Routine(models.Model):
    class Type(models.TextChoices):
        CHECK = 'check', _('Check')
        TIME = 'time', _('Time')
        COUNT = 'count', _('Count')

    class Measure(models.TextChoices):
        SECONDS = 'sec', _('Seconds')
        MINUTES = 'min', _('Minutes')
        HOURS = 'hrs', _('Hours')
        REPS = 'rps', _('Reps')
        SETS = 'sts', _('Sets')

    group = models.ForeignKey(RoutineGroup, on_delete=models.CASCADE, related_name='routines')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)

    type = models.CharField(max_length=5, choices=Type.choices, default=Type.CHECK)
    has_goal = models.BooleanField(default=False)
    goal = models.PositiveIntegerField(blank=True, null=True)
    measure = models.CharField(max_length=50, blank=True, choices=Measure.choices, default=Measure.SECONDS)

    def _calculate_general_statistics(self, entries: 'models.QuerySet[RoutineEntry]') -> Dict[str, Union[int, float]]:
        total = len(entries)
        completed = len([entry for entry in entries if entry.value >= self.goal])
        average = sum([entry.value for entry in entries]) / total
        best = max([entry.value for entry in entries])
        worst = min([entry.value for entry in entries])

        return {
            'total': total,
            'completed': completed,
            'average': average,
            'best': best,
            'worst': worst,
        }

    def _calculate_streak(self, entries: 'models.QuerySet[RoutineEntry]', start: date) -> StreakStatistics:
        # Ensure entries are sorted by date
        dates = [entry.date for entry in entries]

        total = len(entries)
        end_date = date.today()
        missed = (end_date - start).days - total
        streak_days = 0

        current_date = end_date - timedelta(days=1)  # Exclude today

        for entry_date in dates:
            if entry_date == current_date:
                streak_days += 1
                current_date -= timedelta(days=1)
            else:
                break

        return {
            'missed': missed,
            'completeness': streak_days / total,
            'days': streak_days,
            'start': current_date,
            'end': end_date,
        }

    def statistics(
        self, start: date, end: date = None
    ) -> Union[Tuple[RoutineStatistics, 'models.QuerySet[Routine]'], None]:
        """Calculate statistics for this routine within a given date range.

        Args:
            start (date): Start date for the statistics.
            end (date, optional): End date for the stastics. Defaults to None.

        Returns:
            Union[Tuple[RoutineStatistics, QuerySet[Routine]], None]:
            Tuple containing the statistics and the entries for the routine.
        """

        # Get all entries for this routine
        # If an end date is not provided, return all entries after the start date
        query = self.entries.order_by('-date')

        if end is not None:
            entries = query.filter(date__range=[start, end])
        else:
            entries = query.filter(date__gte=start)

        # If there are no entries, return None
        if not entries:
            return None

        # Calculate general statistics
        general_stats = self._calculate_general_statistics(entries)

        # Calculate streak
        streak = self._calculate_streak(entries, start)

        # Return statistics
        return {**general_stats, 'streak': streak}, entries

    def __str__(self):
        return self.name


class RoutineEntry(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='entries')
    date = models.DateField()
    value = models.PositiveIntegerField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.routine.name} - {self.date}'

    class Meta:
        ordering = ['-date']

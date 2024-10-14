from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


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

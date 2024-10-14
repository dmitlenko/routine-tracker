import math

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import now, timedelta

from .models import Routine, RoutineEntry, RoutineGroup

User = get_user_model()


class RoutineGroupModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user1@example.com', password='pass123')

    def test_create_routine_group_success(self):
        group = RoutineGroup.objects.create(user=self.user, name='Morning Routine')
        self.assertEqual(RoutineGroup.objects.count(), 1)
        self.assertEqual(str(group), 'Morning Routine')

    def test_group_name_max_length(self):
        group = RoutineGroup(user=self.user, name='a' * 101)  # Exceeding max length
        with self.assertRaises(ValidationError):
            group.full_clean()  # Validates field length

    def test_optional_fields(self):
        group = RoutineGroup.objects.create(user=self.user, name='Evening Routine', icon='', description='')
        self.assertEqual(group.icon, '')
        self.assertEqual(group.description, '')

    def test_user_deletion_cascades_groups(self):
        RoutineGroup.objects.create(user=self.user, name='Routine')
        self.user.delete()
        self.assertEqual(RoutineGroup.objects.count(), 0)


class RoutineModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user1@example.com', password='pass123')
        self.group = RoutineGroup.objects.create(user=self.user, name='Morning Routine')

    def test_create_routine_success(self):
        routine = Routine.objects.create(group=self.group, name='Push-ups')
        self.assertEqual(Routine.objects.count(), 1)
        self.assertEqual(str(routine), 'Push-ups')

    def test_routine_default_type_and_measure(self):
        routine = Routine.objects.create(group=self.group, name='Check In')
        self.assertEqual(routine.type, Routine.Type.CHECK)
        self.assertEqual(routine.measure, Routine.Measure.SECONDS)

    def test_invalid_type_choice(self):
        routine = Routine(group=self.group, name='Invalid Routine', type='invalid')
        with self.assertRaises(ValidationError):
            routine.full_clean()  # Validates the 'type' field choices

    def test_optional_goal_and_measure(self):
        routine = Routine.objects.create(group=self.group, name='Jogging', has_goal=True, goal=5000, measure='min')
        self.assertTrue(routine.has_goal)
        self.assertEqual(routine.goal, 5000)
        self.assertEqual(routine.measure, Routine.Measure.MINUTES)

    def test_null_goal_when_has_goal_false(self):
        routine = Routine.objects.create(group=self.group, name='Stretching', has_goal=False, goal=None)
        self.assertIsNone(routine.goal)

    def test_group_deletion_cascades_routines(self):
        Routine.objects.create(group=self.group, name='Sit-ups')
        self.group.delete()
        self.assertEqual(Routine.objects.count(), 0)


class RoutineEntryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user1@example.com', password='pass123')
        self.group = RoutineGroup.objects.create(user=self.user, name='Morning Routine')
        self.routine = Routine.objects.create(
            group=self.group, name='Push-ups', has_goal=True, goal=100, measure='rps'
        )

    def test_create_routine_entry_success(self):
        entry = RoutineEntry.objects.create(routine=self.routine, date=now().date(), value=50)
        self.assertEqual(RoutineEntry.objects.count(), 1)
        self.assertEqual(entry.value, 50)

    def test_entry_ordering_by_date(self):
        entry1 = RoutineEntry.objects.create(routine=self.routine, date=now().date() - timedelta(days=1), value=20)
        entry2 = RoutineEntry.objects.create(routine=self.routine, date=now().date(), value=30)
        self.assertEqual(list(RoutineEntry.objects.all()), [entry2, entry1])  # Ordered by date descending

    def test_entry_value_must_be_positive(self):
        entry = RoutineEntry(routine=self.routine, date=now().date(), value=-5)
        with self.assertRaises(ValidationError):
            entry.full_clean()  # Validates that value is positive

    def test_notes_field_optional(self):
        entry = RoutineEntry.objects.create(routine=self.routine, date=now().date(), value=10, notes='')
        self.assertEqual(entry.notes, '')

    def test_routine_deletion_cascades_entries(self):
        RoutineEntry.objects.create(routine=self.routine, date=now().date(), value=25)
        self.routine.delete()
        self.assertEqual(RoutineEntry.objects.count(), 0)

    def test_multiple_entries_for_same_day(self):
        RoutineEntry.objects.create(routine=self.routine, date=now().date(), value=10)
        RoutineEntry.objects.create(routine=self.routine, date=now().date(), value=20)
        self.assertEqual(RoutineEntry.objects.count(), 2)


class RoutineStatisticsTest(TestCase):
    entries = 7
    streak_days = 3
    amplitude = 20

    def setUp(self):
        # Some setup code to create a user, group, routine, and entries
        # Variables used to create and test entries
        self.skip_days = {self.streak_days + 1, 7}
        self.total = self.entries - len(self.skip_days)
        self.start_date = now().date() - timedelta(days=self.entries)
        self.end_date = now().date() - timedelta(days=3)
        self.f = lambda x: math.ceil(self.amplitude * math.log(x + 1))  # Logarithmic function

        # Create user, group, and routine
        self.user = User.objects.create_user(email='test@email.com', password='pass123')
        self.group = RoutineGroup.objects.create(user=self.user, name='Morning Routine')
        self.routine = Routine.objects.create(
            group=self.group, name='Push-ups', has_goal=True, goal=14, measure=Routine.Measure.REPS
        )

        # Create entries for the routine
        for i in range(1, self.entries + 1):
            # Let's skip some days
            if i in self.skip_days:
                continue

            # Use formula to create entries with values that raise in log scale
            RoutineEntry.objects.create(
                routine=self.routine,
                date=now().date() - timedelta(days=i),
                value=self.f(i),  # this makes me feel like a genius
            )

    def test_statistics_total(self):
        stats, _ = self.routine.statistics(start=self.start_date)
        self.assertEqual(stats['total'], self.total)

    def test_statistics_completed(self):
        stats, entries = self.routine.statistics(start=self.start_date)
        completed = len([entry for entry in entries if entry.value >= self.routine.goal])
        self.assertEqual(stats['completed'], completed)

    def test_statistics_average(self):
        stats, entries = self.routine.statistics(start=self.start_date)
        average = sum([entry.value for entry in entries]) / self.total
        self.assertEqual(stats['average'], average)

    def test_statistics_best(self):
        stats, entries = self.routine.statistics(start=self.start_date)
        best = max([entry.value for entry in entries])
        self.assertEqual(stats['best'], best)

    def test_statistics_worst(self):
        stats, entries = self.routine.statistics(start=self.start_date)
        worst = min([entry.value for entry in entries])
        self.assertEqual(stats['worst'], worst)

    def test_statistics_no_entries(self):
        stats = self.routine.statistics(start=now().date())
        self.assertIsNone(stats)

    def test_statistics_end_date(self):
        stats, entries = self.routine.statistics(start=self.start_date, end=self.end_date)
        total = len(entries)
        completed = len([entry for entry in entries if entry.value >= self.routine.goal])
        average = sum([entry.value for entry in entries]) / total
        best = max([entry.value for entry in entries])
        worst = min([entry.value for entry in entries])

        self.assertEqual(
            stats['total'], (self.end_date - self.start_date).days - 1
        )  # -1 because we skipping day 7 in self.skip_days
        self.assertEqual(stats['completed'], completed)
        self.assertEqual(stats['average'], average)
        self.assertEqual(stats['best'], best)
        self.assertEqual(stats['worst'], worst)

    def test_statistics_streak(self):
        stats, entries = self.routine.statistics(start=self.start_date)
        streak = stats['streak']
        self.assertEqual(streak['missed'], self.total - self.streak_days)
        self.assertEqual(streak['completeness'], self.streak_days / self.total)
        self.assertEqual(streak['days'], 3)
        self.assertEqual(streak['start'], now().date() - timedelta(days=self.streak_days + 1))
        self.assertEqual(streak['end'], now().date())

import random
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from routine_tracker.routines.models import Routine, RoutineEntry, RoutineGroup

User = get_user_model()

fake = Faker()


class Command(BaseCommand):
    help = "Fill database with fake RoutineGroup, Routine, and RoutineEntry data"

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=5, help='Number of users to generate data for')
        parser.add_argument('--groups', type=int, default=3, help='Number of routine groups per user')
        parser.add_argument('--routines', type=int, default=5, help='Number of routines per group')
        parser.add_argument('--entries', type=int, default=30, help='Number of entries per routine')

    def handle(self, *args, **kwargs):
        users_count = kwargs['users']
        groups_count = kwargs['groups']
        routines_count = kwargs['routines']
        entries_count = kwargs['entries']

        users = User.objects.all()[:users_count]
        if not users:
            self.stdout.write(self.style.ERROR("No users found. Please create some users first."))
            return

        for user in users:
            for _ in range(groups_count):
                group = RoutineGroup.objects.create(
                    user=user,
                    name=fake.word().capitalize(),
                    description=fake.sentence(),
                    icon=fake.word(),
                    color=fake.color(),
                )
                self.stdout.write(self.style.SUCCESS(f"Created RoutineGroup: {group.name}"))

                for _ in range(routines_count):
                    routine_type = random.choice(Routine.Type.values)

                    routine = Routine.objects.create(
                        group=group,
                        name=fake.word().capitalize(),
                        description=fake.sentence(),
                        icon=fake.word(),
                        type=routine_type,
                        has_goal=random.choice([True, False]),
                        goal=random.randint(10, 100) if random.choice([True, False]) else None,
                        measure=random.choice(Routine.DefaultMeasures.values),
                    )
                    self.stdout.write(self.style.SUCCESS(f"  Created Routine: {routine.name}"))

                    for _ in range(entries_count):
                        entry_date = date.today() - timedelta(days=random.randint(0, 365))
                        value = random.randint(0, 1) if routine.type == Routine.Type.CHECK else random.randint(1, 100)
                        entry = RoutineEntry.objects.create(
                            routine=routine,
                            date=entry_date,
                            value=value,
                            notes=fake.text(max_nb_chars=100),
                        )
                        self.stdout.write(self.style.SUCCESS(f"    Created RoutineEntry on {entry.date}"))

        self.stdout.write(self.style.SUCCESS("Successfully populated the database with fake data."))

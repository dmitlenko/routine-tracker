from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Compile locale files for the project"

    tasks = [
        (("routine_tracker.core.tasks.send_reminders", "Send reminders"), (24, IntervalSchedule.HOURS)),
    ]

    def handle(self, *args, **options):
        # Delete all periodic tasks
        IntervalSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()

        for (task, name), (every, period) in self.tasks:
            schedule = IntervalSchedule.objects.create(every=every, period=period)
            PeriodicTask.objects.create(
                interval=schedule,
                name=name,
                task=task,
            )

            self.stdout.write(self.style.SUCCESS(f"Created task: {name}"))

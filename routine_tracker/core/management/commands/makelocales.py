from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create locale files for the project'

    def handle(self, *args, **options):
        call_command(
            'makemessages',
            all=True,
            ignore=['venv'],
            verbosity=1,
        )
